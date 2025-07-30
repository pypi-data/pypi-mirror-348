"""
Redis 服務管理模組，負責啟動 Redis 服務並提供連接池和基本操作
"""
import json
import subprocess
import time
import redis
from typing import Optional, Any, Tuple

from .utils import logger
from .settings import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD

# Redis 連接池
_redis_pool = None
_redis_process = None
# 模擬 Redis 實例
_fake_redis = None
# 是否使用模擬 Redis
_use_fake_redis = False


def is_redis_running(host: str = REDIS_HOST, port: int = REDIS_PORT) -> bool:
    """檢查 Redis 是否在運行中"""
    try:
        r = redis.Redis(
            host=host,
            port=port,
            db=REDIS_DB,
            password=REDIS_PASSWORD,
            socket_timeout=1
        )
        return r.ping()
    except (redis.ConnectionError, redis.TimeoutError, ConnectionRefusedError):
        return False


def start_redis_server(port: int = REDIS_PORT) -> Tuple[bool, Optional[subprocess.Popen]]:
    """啟動 Redis 服務器

    如果本地沒有安裝 Redis，將嘗試從 Python 包啟動嵌入式 Redis 服務
    如果 Redis 已經在運行，則直接使用已有的服務

    Args:
        port: Redis 服務器端口

    Returns:
        Tuple: (已啟動或運行中, 進程對象)
        進程對象在服務已運行時為 None
    """
    global REDIS_PORT, _redis_process, _use_fake_redis, _fake_redis
    REDIS_PORT = port

    # 檢查 Redis 是否已經在運行
    if is_redis_running(port=port):
        logger.info(f"Redis 已在運行於 {REDIS_HOST}:{port}")
        return True, None

    logger.info("嘗試啟動 Redis 服務器...")

    # 首先嘗試使用 redis-server 啟動
    try:
        # 嘗試使用系統 redis-server 命令
        cmd = ["redis-server", "--port", str(port)]
        redis_process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # 等待 Redis 啟動 (最多等待 3 秒)
        for _ in range(30):
            time.sleep(0.1)
            if is_redis_running(port=port):
                logger.info(f"Redis 服務器已啟動於 {REDIS_HOST}:{port}")
                _redis_process = redis_process
                return True, redis_process
    except (FileNotFoundError, subprocess.SubprocessError):
        logger.warning("無法使用系統 redis-server 啟動 Redis")

    # 如果系統沒有 redis-server，嘗試使用 redis-server-bin 包
    try:
        import importlib.util
        if importlib.util.find_spec("redis_server_bin"):
            from redis_server_bin import run_server
            # 啟動服務但在背景執行
            thread = run_server(port=port, daemonize=True)
            # 等待 Redis 啟動
            for _ in range(30):
                time.sleep(0.1)
                if is_redis_running(port=port):
                    logger.info(f"Redis 服務器(內嵌)已啟動於 {REDIS_HOST}:{port}")
                    _redis_process = thread
                    return True, thread
    except ImportError:
        logger.warning(
            "無法使用 redis-server-bin 包，將嘗試使用模擬 Redis"
        )

    # 如果都失敗了，嘗試使用 fakeredis 模擬 Redis
    try:
        import fakeredis
        logger.info("使用 fakeredis 模擬 Redis 服務")
        _fake_redis = fakeredis.FakeServer()
        _use_fake_redis = True
        return True, None
    except ImportError:
        logger.error("無法啟動 Redis 服務，請安裝 redis-server-bin 或 fakeredis")

    return False, None


def get_redis_connection() -> redis.Redis:
    """獲取 Redis 連接

    Returns:
        Redis 連接物件
    """
    global _redis_pool, _fake_redis, _use_fake_redis

    # 如果使用模擬 Redis
    if _use_fake_redis:
        try:
            import fakeredis
            logger.debug("使用 fakeredis 連接")
            return fakeredis.FakeRedis(server=_fake_redis, decode_responses=True)
        except ImportError:
            logger.error("fakeredis 模組不可用")
            raise RuntimeError("Redis 連接失敗")

    # 如果連接池不存在或已關閉，創建新的連接池
    if _redis_pool is None:
        _redis_pool = redis.ConnectionPool(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            password=REDIS_PASSWORD,
            decode_responses=True  # 自動將 bytes 轉為 str
        )

    return redis.Redis(connection_pool=_redis_pool)


def set_redis_key(key: str, value: Any, expire: Optional[int] = None) -> bool:
    """設置 Redis 鍵值

    Args:
        key: 鍵名
        value: 值 (將自動轉換為 JSON 字符串)
        expire: 過期時間 (秒)，None 表示永不過期

    Returns:
        是否成功設置
    """
    try:
        r = get_redis_connection()
        # 將複雜數據結構轉為 JSON
        if not isinstance(value, (str, int, float, bool)):
            value = json.dumps(value)
        r.set(key, value)
        if expire is not None:
            r.expire(key, expire)
        return True
    except Exception as e:
        logger.error(f"設置 Redis 鍵 {key} 時出錯: {str(e)}")
        return False


def get_redis_key(key: str, default: Any = None) -> Any:
    """獲取 Redis 鍵值

    Args:
        key: 鍵名
        default: 如果鍵不存在，返回的默認值

    Returns:
        鍵值，如果值為 JSON 字符串會自動解析為 Python 對象
    """
    try:
        r = get_redis_connection()
        value = r.get(key)
        if value is None:
            return default

        # 嘗試解析 JSON
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value
    except Exception as e:
        logger.error(f"獲取 Redis 鍵 {key} 時出錯: {str(e)}")
        return default


def delete_redis_key(key: str) -> bool:
    """刪除 Redis 鍵

    Args:
        key: 鍵名

    Returns:
        是否成功刪除
    """
    try:
        r = get_redis_connection()
        r.delete(key)
        return True
    except Exception as e:
        logger.error(f"刪除 Redis 鍵 {key} 時出錯: {str(e)}")
        return False


async def stop_redis_server():
    """停止 Redis 服務器"""
    global _redis_process, _use_fake_redis, _fake_redis
    if _redis_process is not None:
        logger.info("正在停止 Redis 服務器...")
        _redis_process.terminate()
        _redis_process.wait()
        _redis_process = None
        logger.info("Redis 服務器已停止")

    # 清理模擬 Redis
    if _use_fake_redis and _fake_redis is not None:
        logger.info("清理模擬 Redis 資源")
        _fake_redis = None
        _use_fake_redis = False


def close_redis_pool():
    """關閉 Redis 連接池"""
    global _redis_pool
    if _redis_pool is not None:
        logger.info("正在關閉 Redis 連接池...")
        _redis_pool.disconnect()
        _redis_pool = None
        logger.info("Redis 連接池已關閉")


def cleanup_redis():
    """清理 Redis 資源"""
    close_redis_pool()
    stop_redis_server()
