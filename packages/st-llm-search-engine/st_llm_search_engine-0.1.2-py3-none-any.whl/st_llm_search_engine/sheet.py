"""
Google Sheet 整合模組 - 高效緩存和多進程支援
"""
import os
import time
import json
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any

# 嘗試導入 pandas
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

# 嘗試導入 Google API 庫
try:
    import gspread
    from google.oauth2 import service_account
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False

# API 相關庫
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import traceback

# 從設定模組導入相關設定
from st_llm_search_engine.utils import get_logger
from st_llm_search_engine.redis import (
    get_redis_connection,
    set_redis_key,
    get_redis_key
)

# 設置緩存過期時間
SAVED_SEARCH_EXPIRY = 15 * 60  # 15 分鐘
KOL_EXPIRY = 60 * 60  # 60 分鐘
KOL_DATA_EXPIRY = 15 * 60  # 15 分鐘

# 獲取日誌記錄器
logger = get_logger("sheet")

# 創建路由器
router = APIRouter(prefix="/sheet", tags=["sheet"])


class SheetConnector:
    """Google Sheet 連接器類"""

    def __init__(self, sheet_id: str, tab_name: str, credentials_path: str):
        self.sheet_id = sheet_id
        self.tab_name = tab_name
        self.credentials_path = credentials_path
        self._client = None

    def connect(self) -> bool:
        """建立 Google Sheet 連接"""
        if not GOOGLE_API_AVAILABLE:
            logger.error("Google API 庫未安裝，請執行：poetry add gspread google-auth")
            return False

        if not os.path.exists(self.credentials_path):
            logger.error(f"認證文件不存在：{self.credentials_path}")
            return False

        try:
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path,
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            self._client = gspread.authorize(credentials)
            return True
        except Exception as e:
            logger.error(f"連接 Google Sheet 失敗：{str(e)}")
            return False

    def get_data(self) -> List[Dict[str, Any]]:
        """獲取工作表數據並轉換為字典列表"""
        if not self._client:
            if not self.connect():
                return []

        try:
            sheet = self._client.open_by_key(self.sheet_id).worksheet(self.tab_name)
            data = sheet.get_all_records()
            return data
        except Exception as e:
            logger.error(f"獲取 Sheet 數據失敗：{str(e)}")
            return []


class SheetManager:
    """Google Sheet 管理類，處理配置和緩存"""

    def __init__(self):
        self._kol_config = {"sheet_id": "", "tab_name": "", "service_account_path": ""}
        self._saved_search_config = {"sheet_id": "", "tab_name": "", "service_account_path": ""}
        self._kol_data_config = {"sheet_id": "", "tab_name": "", "service_account_path": ""}

        self._kol_connector = None
        self._saved_search_connector = None
        self._kol_data_connector = None

    def kol_connect(self, sheet_id: str, tab_name: str, credentials_path: str) -> None:
        """設定 KOL Sheet 連接配置"""
        self._kol_config = {
            "sheet_id": sheet_id,
            "tab_name": tab_name,
            "service_account_path": credentials_path
        }

        # 更新環境變數
        os.environ["SHEET_ID"] = sheet_id
        os.environ["SHEET_TAB"] = tab_name
        os.environ["SHEET_CREDENTIALS"] = credentials_path

        # 創建連接器
        self._kol_connector = SheetConnector(sheet_id, tab_name, credentials_path)
        logger.info(f"已設置 KOL Sheet: ID={sheet_id}, Tab={tab_name}")

    def saved_search_connect(self, sheet_id: str, tab_name: str, credentials_path: str) -> None:
        """設定已保存搜索 Sheet 連接配置"""
        self._saved_search_config = {
            "sheet_id": sheet_id,
            "tab_name": tab_name,
            "service_account_path": credentials_path
        }

        os.environ["SAVED_SEARCH_SHEET_ID"] = sheet_id
        os.environ["SAVED_SEARCH_TAB"] = tab_name
        os.environ["SAVED_SEARCH_CREDENTIALS"] = credentials_path

        self._saved_search_connector = SheetConnector(sheet_id, tab_name, credentials_path)
        logger.info(f"已設置 Saved Search Sheet: ID={sheet_id}, Tab={tab_name}")

    def kol_data_connect(self, sheet_id: str, tab_name: str, credentials_path: str) -> None:
        """設定 KOL 數據 Sheet 連接配置"""
        self._kol_data_config = {
            "sheet_id": sheet_id,
            "tab_name": tab_name,
            "service_account_path": credentials_path
        }

        os.environ["KOL_DATA_SHEET_ID"] = sheet_id
        os.environ["KOL_DATA_TAB"] = tab_name
        os.environ["KOL_DATA_CREDENTIALS"] = credentials_path

        self._kol_data_connector = SheetConnector(sheet_id, tab_name, credentials_path)
        logger.info(f"已設置 KOL Data Sheet: ID={sheet_id}, Tab={tab_name}")

    def get_kol_data(self, force_refresh: bool = False) -> List[Dict[str, Any]]:
        """使用 Redis 緩存獲取 KOL 數據"""
        cache_key = "sheet:kol_data"
        redis = get_redis_connection()

        if not force_refresh:
            cached_data = get_redis_key(cache_key)
            if cached_data:
                logger.debug("使用緩存的 KOL 數據")
                return json.loads(cached_data)

        # 緩存不存在或強制刷新，從 Sheet 獲取數據
        with redis.lock("sheet:kol_data_lock", timeout=60):
            # 再次檢查，避免在等待鎖時數據已被其他進程更新
            if not force_refresh:
                cached_data = get_redis_key(cache_key)
                if cached_data:
                    return json.loads(cached_data)

            if not self._kol_data_connector:
                config = self.get_kol_data_config()
                self._kol_data_connector = SheetConnector(
                    config["sheet_id"], config["tab_name"], config["service_account_path"]
                )

            logger.info("從 Google Sheet 獲取最新 KOL 數據")
            data = self._kol_data_connector.get_data()

            # 更新緩存
            set_redis_key(cache_key, json.dumps(data), KOL_DATA_EXPIRY)

            return data

    def get_kol_info(self, force_refresh: bool = False) -> List[Dict[str, Any]]:
        """使用 Redis 緩存獲取 KOL 信息"""
        cache_key = "sheet:kol_info"
        redis = get_redis_connection()

        if not force_refresh:
            cached_data = get_redis_key(cache_key)
            if cached_data:
                logger.debug("使用緩存的 KOL 信息")
                return json.loads(cached_data)

        # 緩存不存在或強制刷新，從 Sheet 獲取數據
        with redis.lock("sheet:kol_info_lock", timeout=30):
            # 再次檢查
            if not force_refresh:
                cached_data = get_redis_key(cache_key)
                if cached_data:
                    return json.loads(cached_data)

            if not self._kol_connector:
                config = self.get_kol_sheet_config()
                self._kol_connector = SheetConnector(
                    config["sheet_id"], config["tab_name"], config["service_account_path"]
                )

            logger.info("從 Google Sheet 獲取最新 KOL 信息")
            data = self._kol_connector.get_data()

            # 標準化欄位
            standardized_data = []
            for record in data:
                new_record = dict(record)  # 複製原始記錄

                # 確保有 kol_id
                if 'kol_id' not in new_record and 'KOL_ID' in new_record:
                    new_record['kol_id'] = new_record['KOL_ID']

                # 確保有 kol_name
                if 'kol_name' not in new_record:
                    if 'KOL' in new_record:
                        new_record['kol_name'] = new_record['KOL']
                    elif 'KOL' in new_record:
                        new_record['kol_name'] = new_record['KOL']

                standardized_data.append(new_record)

            # 更新緩存
            set_redis_key(cache_key, json.dumps(standardized_data), KOL_EXPIRY)

            return standardized_data

    def get_saved_searches(self, force_refresh: bool = False) -> List[Dict[str, Any]]:
        """使用 Redis 緩存獲取已保存的搜索記錄"""
        cache_key = "sheet:saved_searches"
        redis = get_redis_connection()

        if not force_refresh:
            cached_data = get_redis_key(cache_key)
            if cached_data:
                logger.debug("使用緩存的已保存搜索")
                return json.loads(cached_data)

        # 緩存不存在或強制刷新，從 Sheet 獲取數據
        with redis.lock("sheet:saved_searches_lock", timeout=30):
            # 再次檢查
            if not force_refresh:
                cached_data = get_redis_key(cache_key)
                if cached_data:
                    return json.loads(cached_data)

            if not self._saved_search_connector:
                config = self.get_saved_search_config()
                self._saved_search_connector = SheetConnector(
                    config["sheet_id"], config["tab_name"], config["service_account_path"]
                )

            logger.info("從 Google Sheet 獲取最新已保存搜索")
            data = self._saved_search_connector.get_data()

            # 更新緩存
            set_redis_key(cache_key, json.dumps(data), SAVED_SEARCH_EXPIRY)

            return data

    def get_filtered_kol_data(
        self,
        time_range: Dict[str, int],
        kol_ids: List[str] = None,
        prompt: str = ""
    ) -> Dict[str, Any]:
        """根據時間範圍和KOL ID列表篩選KOL數據"""
        if not PANDAS_AVAILABLE:
            logger.error("pandas 未安裝，請執行：poetry add pandas")
            return {"error": "數據處理組件缺失", "records": []}

        # 獲取請求參數
        start_time = time_range.get("start_time")
        end_time = time_range.get("end_time")
        if start_time is None or end_time is None:
            return {"error": "缺少時間範圍參數", "records": []}

        # 默認值處理
        if kol_ids is None:
            kol_ids = ["All"]

        # 記錄篩選條件
        logger.info(f"篩選條件: 時間={start_time}~{end_time}, KOL={kol_ids}")

        # 獲取KOL數據
        kol_data = self.get_kol_data()
        if not kol_data:
            return {
                "records": [],
                "total_count": 0,
                "filter_info": {
                    "time_range": self._format_time_range(start_time, end_time),
                    "kol_ids": kol_ids,
                    "prompt": prompt
                }
            }

        # 獲取KOL映射數據
        kol_records = self.get_kol_info()

        # 使用pandas處理數據
        data_df = pd.DataFrame(kol_data)
        if data_df.empty:
            return {
                "records": [],
                "total_count": 0,
                "filter_info": {
                    "time_range": self._format_time_range(start_time, end_time),
                    "kol_ids": kol_ids,
                    "prompt": prompt
                }
            }

        # 確保時間戳為數值型
        if 'timestamp' in data_df.columns:
            data_df['timestamp'] = pd.to_numeric(data_df['timestamp'], errors='coerce')
            data_df = data_df.dropna(subset=['timestamp'])
            logger.info(f"有效時間戳數據: {len(data_df)}筆")

        # 1. 先進行KOL篩選
        if "All" not in kol_ids and 'kol_id' in data_df.columns:
            before_count = len(data_df)
            data_df = data_df[data_df['kol_id'].isin(kol_ids)]
            logger.info(f"KOL篩選: {before_count} -> {len(data_df)}筆")

        # 2. 再進行時間戳篩選
        if 'timestamp' in data_df.columns:
            before_count = len(data_df)
            data_df = data_df[(data_df['timestamp'] >= start_time) & (data_df['timestamp'] <= end_time)]
            logger.info(f"時間篩選: {before_count} -> {len(data_df)}筆")

        # 3. 文本搜索（如果提供了查詢字符串）
        if prompt and 'content' in data_df.columns:
            before_count = len(data_df)
            data_df = data_df[data_df['content'].str.contains(prompt, case=False, na=False)]
            logger.info(f"關鍵詞篩選: {before_count} -> {len(data_df)}筆")

        # 合併 KOL 名稱 - 簡化版，直接使用 merge
        if kol_records and not data_df.empty:
            kol_df = pd.DataFrame(kol_records)

            kol_df.rename(columns={'KOL': 'kol_name'}, inplace=True)

            data_df = data_df.merge(
                kol_df[['kol_id', 'kol_name']],
                on='kol_id',
                how='left'
            )
            # 填充空值
            data_df['kol_name'] = data_df['kol_name'].fillna(data_df['kol_id'])

        # 格式化時間戳
        if 'timestamp' in data_df.columns:
            data_df["created_time"] = data_df["timestamp"].apply(self._format_timestamp)

        # 處理缺失值並按時間戳降序排序
        data_df = data_df.fillna("")
        if 'timestamp' in data_df.columns:
            data_df = data_df.sort_values("timestamp", ascending=False)

        # 選擇需要的列
        columns = ["doc_id", "kol_name", "created_time", "post_url", "content", "reaction_count", "share_count"]
        for col in columns:
            if col not in data_df.columns:
                data_df[col] = ""

        # 轉換為字典列表
        filtered_data = data_df[columns].to_dict(orient="records")
        logger.info(f"篩選後: {len(filtered_data)}筆記錄")

        # 構建響應數據
        response_data = {
            "records": filtered_data,
            "filter_info": {
                "time_range": self._format_time_range(start_time, end_time),
                "kol_ids": kol_ids,
                "prompt": prompt
            },
            "total_count": len(filtered_data)
        }

        return response_data

    def _format_timestamp(self, ts):
        """將時間戳格式化為人類可讀格式"""
        if pd.isna(ts):
            return ""
        try:
            dt = datetime.fromtimestamp(ts, tz=timezone.utc)
            dt = dt.astimezone(timezone(timedelta(hours=8)))
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            return str(ts)

    def _format_time_range(self, start_time: int, end_time: int) -> Dict[str, Any]:
        """格式化時間範圍為人類可讀格式"""
        start_dt_utc8 = datetime.fromtimestamp(start_time, tz=timezone.utc).astimezone(timezone(timedelta(hours=8)))
        end_dt_utc8 = datetime.fromtimestamp(end_time, tz=timezone.utc).astimezone(timezone(timedelta(hours=8)))

        return {
            "start_time": start_time,
            "end_time": end_time,
            "start_time_utc8": start_dt_utc8.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time_utc8": end_dt_utc8.strftime("%Y-%m-%d %H:%M:%S")
        }

    def get_kol_sheet_config(self) -> Dict[str, str]:
        """獲取 KOL Sheet 配置"""
        sheet_id = os.environ.get("SHEET_ID", self._kol_config.get("sheet_id", ""))
        tab_name = os.environ.get("SHEET_TAB", self._kol_config.get("tab_name", ""))
        credentials = os.environ.get(
            "SHEET_CREDENTIALS",
            self._kol_config.get("service_account_path", "")
        )

        return {
            "sheet_id": sheet_id,
            "tab_name": tab_name,
            "service_account_path": credentials
        }

    def get_saved_search_config(self) -> Dict[str, str]:
        """獲取已保存搜索 Sheet 配置"""
        sheet_id = os.environ.get("SAVED_SEARCH_SHEET_ID", self._saved_search_config.get("sheet_id", ""))
        tab_name = os.environ.get("SAVED_SEARCH_TAB", self._saved_search_config.get("tab_name", ""))
        credentials = os.environ.get(
            "SAVED_SEARCH_CREDENTIALS",
            self._saved_search_config.get("service_account_path", "")
        )

        return {
            "sheet_id": sheet_id,
            "tab_name": tab_name,
            "service_account_path": credentials
        }

    def get_kol_data_config(self) -> Dict[str, str]:
        """獲取 KOL 數據 Sheet 配置"""
        sheet_id = os.environ.get("KOL_DATA_SHEET_ID", self._kol_data_config.get("sheet_id", ""))
        tab_name = os.environ.get("KOL_DATA_TAB", self._kol_data_config.get("tab_name", ""))
        credentials = os.environ.get(
            "KOL_DATA_CREDENTIALS",
            self._kol_data_config.get("service_account_path", "")
        )

        return {
            "sheet_id": sheet_id,
            "tab_name": tab_name,
            "service_account_path": credentials
        }


# 創建全局 Sheet 管理器實例
sheet_manager = SheetManager()

# 為了向後兼容，保留原有的接口
sheet = sheet_manager

# 為了向後兼容，保留原有的函數
get_kol_sheet_config = sheet_manager.get_kol_sheet_config
get_saved_search_config = sheet_manager.get_saved_search_config
get_kol_data_config = sheet_manager.get_kol_data_config


# ====================== API 端點 ======================

@router.post("/filtered-kol-data")
async def get_filtered_kol_data(request: Request):
    """根據時間範圍和KOL ID列表篩選KOL數據"""
    try:
        data = await request.json()

        # 獲取請求參數
        time_range = data.get("time_range", {})
        kol_ids = data.get("kol_ids", ["All"])
        prompt = data.get("query", "")

        # 檢查時間範圍
        start_time = time_range.get("start_time")
        end_time = time_range.get("end_time")
        if start_time is None or end_time is None:
            return JSONResponse({"error": "缺少時間範圍參數"}, status_code=400)

        # 使用 SheetManager 處理數據
        result = sheet_manager.get_filtered_kol_data(
            time_range=time_range,
            kol_ids=kol_ids,
            prompt=prompt
        )

        return JSONResponse(result)

    except Exception as e:
        traceback.print_exc()
        logger.error(f"篩選KOL數據時出錯: {str(e)}")
        return JSONResponse({"error": str(e)}, status_code=500)

@router.get("/kol-list")
async def get_kol_list():
    """獲取所有 KOL 的列表"""
    try:
        # 獲取 KOL 數據
        kol_data = sheet_manager.get_kol_info()

        # 提取需要的欄位
        result = []
        for kol in kol_data:
            kol_id = kol.get('kol_id')
            if not kol_id:
                continue

            # 構建基本數據
            kol_info = {
                "kol_id": kol_id,
                "kol_name": kol.get('kol_name', kol.get('KOL', kol_id)),
                "url": kol.get('url', '')
            }

            # 添加標籤
            if 'tag' in kol:
                kol_info['tag'] = kol['tag']

            result.append(kol_info)

        return JSONResponse({"kols": result, "total": len(result)})

    except Exception as e:
        traceback.print_exc()
        logger.error(f"獲取KOL列表時出錯: {str(e)}")
        return JSONResponse({"error": str(e)}, status_code=500)

@router.get("/saved-searches")
async def get_saved_searches():
    """獲取已保存的搜索列表"""
    try:
        # 獲取已保存搜索
        searches = sheet_manager.get_saved_searches()

        return JSONResponse({
            "searches": searches,
            "total": len(searches)
        })

    except Exception as e:
        traceback.print_exc()
        logger.error(f"獲取已保存搜索時出錯: {str(e)}")
        return JSONResponse({"error": str(e)}, status_code=500)







