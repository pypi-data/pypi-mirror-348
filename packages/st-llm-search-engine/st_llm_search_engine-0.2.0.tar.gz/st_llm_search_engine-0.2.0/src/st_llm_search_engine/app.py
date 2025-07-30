"""
主應用程式模組，管理應用程式的啟動和停止
"""
import os
import signal
import socket
import uvicorn
import threading
from typing import Optional

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from . import utils
from .utils import logger
from .redis import start_redis_server, cleanup_redis
from .session import create_session, get_session, router as session_router
from .settings import (
    get_settings, PID_FILE, REDIS_PORT, LOG_DIR,
)
from .gemini import router as gemini_router
from .sheet import router as sheet_router

# 確保日誌系統已初始化，使用配置的格式
utils.configure_logging()

# 創建 FastAPI 應用實例
app = FastAPI()

# 允許跨域請求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加 API 路由
app.include_router(gemini_router, prefix="/api", tags=["gemini"])
app.include_router(session_router, prefix="/api", tags=["session"])
app.include_router(sheet_router, prefix="/api", tags=["sheet"])

# 根路徑重定向到前端頁面
@app.get("/")
async def index():
    return RedirectResponse(url="/ui/")

# 健康檢查端點
@app.get("/ping")
async def ping():
    settings = get_settings()
    return {"status": "ok", "service": settings.app_name}

# 配置可用功能端點
@app.get("/api/capabilities")
async def get_capabilities():
    """獲取系統功能列表"""
    from .gemini import GEMINI_MODEL

    return {
        "search": True,          # 是否啟用搜索功能
        "chat": True,            # 是否啟用聊天功能
        "session": True,         # 是否啟用會話管理
        "embedding": True,       # 是否啟用嵌入向量功能
        "model": GEMINI_MODEL    # 當前使用的 LLM 模型
    }

# 配置靜態文件服務 (前端文件)
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(current_dir, "frontend/build")

if os.path.exists(frontend_dir):
    app.mount("/ui", StaticFiles(directory=frontend_dir, html=True), name="ui")
    logger.info(f"已掛載前端靜態文件: {frontend_dir}")
else:
    # 如果前端文件不存在，返回一個簡單的提示頁面
    @app.get("/ui/{rest_of_path:path}")
    async def frontend_not_found():
        logger.warning(f"前端文件未找到，目錄 {frontend_dir} 不存在")
        return {
            "message": "前端文件未构建。請先在 frontend 目錄運行 'npm install && npm run build'"
        }


# 應用程序生命週期管理
@app.on_event("startup")
async def startup_event():
    """服務啟動時執行"""
    logger.info("==================================================")
    logger.info("API 服務器啟動")
    logger.info("==================================================")

    settings = get_settings()
    logger.info(f"啟動 {settings.app_name} 服務")
    logger.info(f"服務配置: {settings.model_dump_json()}")

    # 設置會話管理所需的Redis
    redis_success, _ = start_redis_server(port=REDIS_PORT)
    if not redis_success:
        logger.error("Redis 服務器啟動失敗，會話管理將不可用")


@app.on_event("shutdown")
async def shutdown_event():
    """服務停止時執行"""
    logger.info("應用程序關閉，清理資源...")
    cleanup_redis()

    # 刪除PID文件（如果存在）
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)

    logger.info("資源清理完成，服務停止")


# 健康檢查端點
@app.get("/health")
async def health_check(request: Request):
    """系統健康檢查"""
    settings = get_settings()
    return {
        "status": "ok",
        "app_name": settings.app_name,
        "version": "1.0.0",
        "session_management": "enabled"
    }


# 獲取或創建會話
@app.get("/api/session")
async def get_or_create_session(session_id: Optional[str] = None):
    """獲取現有會話或創建新會話

    如果提供session_id且存在，則返回該會話
    如果提供session_id但不存在，則創建該session_id的會話
    如果未提供session_id，則創建新會話
    """
    if session_id:
        session = get_session(session_id)
        if session:
            return {"session_id": session_id, "session": session}
        else:
            new_id = create_session(session_id)
            session = get_session(new_id)
            return {"session_id": new_id, "session": session}
    else:
        new_id = create_session()
        session = get_session(new_id)
        return {"session_id": new_id, "session": session}


def is_port_available(port: int) -> bool:
    """檢查端口是否可用

    Args:
        port: 要檢查的端口號

    Returns:
        如果端口可用返回 True，否則返回 False
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("localhost", port))
            return True
    except OSError:
        return False


def find_available_port(start_port=8000, max_attempts=10):
    port = start_port
    for _ in range(max_attempts):
        if is_port_available(port):
            return port
        port += 1
    raise RuntimeError(f"找不到可用埠口，從 {start_port} 開始試了 {max_attempts} 次")


def write_pid(pid_file: str = PID_FILE):
    """將進程 ID 寫入文件

    Args:
        pid_file: PID 文件路徑
    """
    with open(pid_file, "w") as f:
        f.write(str(os.getpid()))
    logger.info(f"進程 ID {os.getpid()} 已寫入 {pid_file}")

    # 註冊退出時的清理函數
    def cleanup_pid_file():
        if os.path.exists(pid_file):
            os.remove(pid_file)
            logger.info(f"已刪除 PID 文件 {pid_file}")

    signal.signal(signal.SIGTERM, lambda sig, frame: cleanup_pid_file())
    signal.signal(signal.SIGINT, lambda sig, frame: cleanup_pid_file())


# 全局變量追蹤服務器狀態
_server_started = False
_server_url = None

def run_api_server(
    host="127.0.0.1",
    port=8000,
    workers=1,
    kol_sheet_id=None,
    kol_tab=None,
    service_account=None,
    saved_search_sheet_id=None,
    saved_search_tab=None,
    kol_data_sheet_id=None,
    kol_data_tab=None,
    gemini_api_key=None
):
    """
    啟動 API 服務器

    參數:
    - host: 主機地址，預設為 127.0.0.1
    - port: 端口號，預設為 8000
    - workers: 工作進程數，預設為 1
    - kol_sheet_id: KOL 表格 ID
    - kol_tab: KOL 表格頁籤名稱
    - service_account: Google 服務帳號 JSON 文件路徑
    - saved_search_sheet_id: 已保存搜索表格 ID
    - saved_search_tab: 已保存搜索表格頁籤名稱
    - kol_data_sheet_id: KOL 數據表格 ID
    - kol_data_tab: KOL 數據表格頁籤名稱
    - gemini_api_key: Gemini API 金鑰
    """
    global _server_started, _server_url

    # 如果服務器已經啟動，直接返回 URL
    if _server_started:
        return _server_url

    # 設置日誌目錄
    log_dir = LOG_DIR
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "st_llm_search_engine.log")

    # 清空日誌文件
    with open(log_file, "w") as f:
        f.write("")

    # 設置環境變數
    if kol_sheet_id:
        os.environ["SHEET_ID"] = kol_sheet_id
    if kol_tab:
        os.environ["SHEET_TAB"] = kol_tab
    if service_account:
        os.environ["SHEET_CREDENTIALS"] = service_account
    if saved_search_sheet_id:
        os.environ["SAVED_SEARCH_SHEET_ID"] = saved_search_sheet_id
    if saved_search_tab:
        os.environ["SAVED_SEARCH_TAB"] = saved_search_tab
    if kol_data_sheet_id:
        os.environ["KOL_DATA_SHEET_ID"] = kol_data_sheet_id
    if kol_data_tab:
        os.environ["KOL_DATA_TAB"] = kol_data_tab
    if gemini_api_key:
        os.environ["GEMINI_API_KEY"] = gemini_api_key

    # 先檢查端口是否可用
    if not is_port_available(port):
        raise RuntimeError(f"端口 {port} 已被占用，請嘗試其他端口")

    logger.info(f"正在使用端口: {port}")

    # 3) 用同一套 logging 配置啟動 Uvicorn
    config = uvicorn.Config(
        "st_llm_search_engine.app:app",
        host=host,
        port=port,
        workers=workers,
        log_config=None,    # 停用 Uvicorn 預設 log 設定
        access_log=False,   # 不要內建的 access log
    )
    server = uvicorn.Server(config)

    # 4) 背後線程啟動，不阻塞，也不關閉主進程的 event loop
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    # 5) 立刻回傳 URL，前端就能拿到正確的 port
    _server_started = True
    _server_url = f"http://{host}:{port}"
    return _server_url

DEFAULT_PORT = 8001
