"""工具函数模块"""

import os
from dotenv import set_key


def check_api_key(api_key: str) -> str:
    """
    检查 API 密钥是否有效

    Args:
        api_key (str): API 密钥名称

    Returns:
        str: 如果有效返回 API 密钥，否则返回 None
    """

    key = os.getenv(api_key, None)
    if not key or len(key) < 1:
        raise ValueError(f"{api_key} is not set in environment variables.")
    
    return key

def set_api_key(api_key: str, value: str) -> None:
    """
    设置 API 密钥

    Args:
        api_key (str): API 密钥名称
        value (str): API 密钥值
    """
    
    if not api_key or not value:
        raise ValueError("API key and value cannot be empty.")
    
    set_key(".env", api_key, value)
    os.environ[api_key] = value
    
def response_json(status_code: str, message: str, data: dict = {}) -> dict:
    """
    构建 JSON 响应

    Args:
        status_code (str): 状态码，取值："success" 或 "error"
        message (str): 消息
        data (dict): 数据

    Returns:
        str: JSON 响应字符串
    """
    
    return {
        "status_code": status_code,
        "message": message,
        "data": data
    }