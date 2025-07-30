"""
全局設定模組，管理應用程式的所有配置參數
"""
import os
from typing import Dict, Any
from pydantic import BaseModel, Field

# Redis 相關設定
REDIS_HOST = os.environ.get("ST_LLM_REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("ST_LLM_REDIS_PORT", "6379"))
REDIS_DB = 0
REDIS_PASSWORD = os.environ.get("ST_LLM_REDIS_PASSWORD", None)

# Gemini 模型設定
GEMINI_MODEL = os.environ.get("ST_LLM_GEMINI_MODEL", "gemini-2.0-flash")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# 會話設定
DEFAULT_SESSION = "default"
SESSION_EXPIRE = 60 * 60 * 24 * 7  # 7 天
MAX_MESSAGES = 30  # 默認最大消息數量

# 日誌設定
LOG_DIR = "/tmp/st_llm_search_engine"
LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
LOG_BACKUP_COUNT = 10
LOG_LEVEL = os.environ.get("ST_LLM_LOG_LEVEL", "info").lower()

# PID 文件路徑
PID_FILE = f"{LOG_DIR}/server.pid"

# API 設定
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000
DEFAULT_WORKERS = 1


class AppSettings(BaseModel):
    """應用程式設定類，使用 Pydantic 進行驗證"""
    app_name: str = Field(default="ST LLM Search Engine", env="ST_LLM_APP_NAME")
    api_url: str = Field(default="", env="ST_LLM_API_URL")
    debug: bool = Field(default=False, env="ST_LLM_DEBUG")
    workers: int = Field(default=DEFAULT_WORKERS, env="ST_LLM_WORKERS")
    redis_host: str = Field(default=REDIS_HOST, env="ST_LLM_REDIS_HOST")
    redis_port: int = Field(default=REDIS_PORT, env="ST_LLM_REDIS_PORT")
    gemini_model: str = Field(default=GEMINI_MODEL, env="ST_LLM_GEMINI_MODEL")
    gemini_api_key: str = Field(default=GEMINI_API_KEY, env="GEMINI_API_KEY")
    log_level: str = Field(default=LOG_LEVEL, env="ST_LLM_LOG_LEVEL")


def get_settings() -> AppSettings:
    """獲取應用程式設定實例"""
    return AppSettings()


def dict_to_env_vars(config: Dict[str, Any]) -> None:
    """將配置字典轉換為環境變量

    Args:
        config: 配置字典
    """
    import json

    for key, value in config.items():
        env_key = f"ST_LLM_{key.upper()}"
        if isinstance(value, (dict, list)):
            os.environ[env_key] = json.dumps(value)
        elif value is not None:
            os.environ[env_key] = str(value)


# KOL 數據緩存
_kol_data_cache = None
_kol_data_cache_timestamp = 0
