"""
Session 管理模組，基於 Redis 實現多用戶會話管理
"""
import time
import uuid
from typing import Dict, List, Optional, Any, Union
from fastapi import APIRouter, Query
from .redis import set_redis_key, get_redis_key, delete_redis_key
from .utils import logger


# Session 相關配置
SESSION_PREFIX = "session:"         # Redis 中 session 的 key 前綴
MESSAGE_PREFIX = "message:"         # Redis 中消息的 key 前綴
SESSION_EXPIRE = 60 * 60 * 24 * 7   # Session 過期時間 (7天)
DEFAULT_SESSION = "default"         # 默認會話 ID

# 創建路由器
router = APIRouter()

@router.get("/messages")
async def get_session_messages(session_id: str = Query(DEFAULT_SESSION)):
    """獲取會話消息 API 端點

    Args:
        session_id: 會話 ID

    Returns:
        會話消息列表
    """
    logger.info(f"獲取會話消息: {session_id}")
    messages = get_messages(session_id)

    return {
        "session_id": session_id,
        "messages": messages
    }

def generate_session_id() -> str:
    """生成唯一的 session ID

    Returns:
        唯一的 session ID
    """
    return str(uuid.uuid4())


def create_session(session_id: Optional[str] = None) -> str:
    """創建新的會話

    Args:
        session_id: 指定的會話 ID，如果為 None 則自動生成

    Returns:
        會話 ID
    """
    if session_id is None:
        session_id = generate_session_id()

    # 創建 session 記錄
    session_data = {
        "id": session_id,
        "created_at": int(time.time()),
        "updated_at": int(time.time()),
        "message_count": 0
    }

    session_key = f"{SESSION_PREFIX}{session_id}"
    if set_redis_key(session_key, session_data, expire=SESSION_EXPIRE):
        logger.info(f"創建新會話: {session_id}")
        return session_id
    else:
        logger.error(f"創建會話失敗: {session_id}")
        return DEFAULT_SESSION


def get_session(session_id: str) -> Optional[Dict[str, Any]]:
    """獲取會話數據

    Args:
        session_id: 會話 ID

    Returns:
        會話數據，如果不存在則返回 None
    """
    session_key = f"{SESSION_PREFIX}{session_id}"
    session_data = get_redis_key(session_key)

    # 如果會話不存在，則創建一個新的
    if session_data is None:
        new_id = create_session(session_id)
        if new_id != session_id:
            return None
        return get_session(session_id)

    return session_data


def update_session(
    session_id: str,
    **fields: Any
) -> bool:
    """更新會話數據

    Args:
        session_id: 會話 ID
        **fields: 要更新的字段

    Returns:
        是否成功更新
    """
    session_data = get_session(session_id)
    if session_data is None:
        return False

    # 更新字段
    session_data.update(fields)
    session_data["updated_at"] = int(time.time())

    # 保存更新
    session_key = f"{SESSION_PREFIX}{session_id}"
    return set_redis_key(session_key, session_data, expire=SESSION_EXPIRE)


def delete_session(session_id: str) -> bool:
    """刪除會話

    Args:
        session_id: 會話 ID

    Returns:
        是否成功刪除
    """
    # 首先獲取會話，檢查是否存在
    session_data = get_session(session_id)
    if session_data is None:
        return False

    # 刪除會話消息
    message_key = f"{MESSAGE_PREFIX}{session_id}"
    delete_redis_key(message_key)

    # 刪除會話本身
    session_key = f"{SESSION_PREFIX}{session_id}"
    return delete_redis_key(session_key)


def add_message(
    session_id: str,
    role: str,
    content: str,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """添加消息到會話

    Args:
        session_id: 會話 ID
        role: 消息角色 ("user" 或 "bot")
        content: 消息內容
        metadata: 消息元數據 (可選)，用於存儲額外信息，如查詢參數或分析結果

    Returns:
        添加的消息對象
    """
    # 獲取或創建會話
    session_data = get_session(session_id)
    if session_data is None:
        session_id = create_session(session_id)
        session_data = get_session(session_id)

    # 創建新消息
    msg_ts = int(time.time() * 1000)
    msg_count = session_data['message_count'] + 1
    message_id = f"{msg_ts}_{msg_count}"

    # metadata or {} 確保元數據始終是字典，即使傳入的是 None
    # 這樣後續代碼可以直接使用 metadata 而不需要檢查是否為 None
    message = {
        "id": message_id,
        "role": role,
        "content": content,
        "timestamp": int(time.time()),
        "metadata": metadata or {}
    }

    # 獲取會話消息列表
    message_key = f"{MESSAGE_PREFIX}{session_id}"
    messages = get_redis_key(message_key, default=[])

    # 添加新消息
    messages.append(message)

    # 保存消息列表
    success = set_redis_key(message_key, messages, expire=SESSION_EXPIRE)

    if success:
        # 更新會話消息計數
        update_session(session_id, message_count=len(messages))
        logger.info(f"添加消息 {message_id} 到會話 {session_id}")
    else:
        logger.error(f"添加消息到會話 {session_id} 失敗")

    return message


def get_messages(
    session_id: str,
    since_id: Optional[str] = None,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """獲取會話消息

    Args:
        session_id: 會話 ID
        since_id: 只獲取此 ID 之後的消息
        limit: 消息數量限制

    Returns:
        消息列表
    """
    # 檢查會話是否存在
    if get_session(session_id) is None:
        return []

    # 獲取消息列表
    message_key = f"{MESSAGE_PREFIX}{session_id}"
    messages = get_redis_key(message_key, default=[])

    # 篩選 since_id 之後的消息
    if since_id:
        filtered_messages = []
        found = False
        for msg in messages:
            if found:
                filtered_messages.append(msg)
            elif msg["id"] == since_id:
                found = True
        messages = filtered_messages

    # 限制消息數量
    if limit and limit > 0:
        messages = messages[-limit:]

    return messages


def clear_messages(session_id: str) -> bool:
    """清空會話消息

    Args:
        session_id: 會話 ID

    Returns:
        是否成功清空
    """
    # 檢查會話是否存在
    if get_session(session_id) is None:
        return False

    # 清空消息列表
    message_key = f"{MESSAGE_PREFIX}{session_id}"
    success = set_redis_key(message_key, [], expire=SESSION_EXPIRE)

    if success:
        # 更新會話消息計數
        update_session(session_id, message_count=0)
        logger.info(f"清空會話 {session_id} 的消息")

    return success


def get_session_context(
    session_id: str,
    max_messages: Optional[int] = 30
) -> List[Dict[str, Union[str, Dict[str, Any]]]]:
    """獲取會話上下文，適用於 LLM 聊天

    返回的消息格式適用於 LLM API，例如 Gemini

    Args:
        session_id: 會話 ID
        max_messages: 最大消息數量，默認獲取最近30條消息

    Returns:
        LLM 聊天上下文
    """
    messages = get_messages(session_id, limit=max_messages)

    # 轉換為 LLM 聊天格式
    context = []
    for msg in messages:
        role = "user" if msg["role"] == "user" else "model"
        context.append({
            "role": role,
            "content": msg["content"],
            "parts": [{"text": msg["content"]}]
        })

    return context
