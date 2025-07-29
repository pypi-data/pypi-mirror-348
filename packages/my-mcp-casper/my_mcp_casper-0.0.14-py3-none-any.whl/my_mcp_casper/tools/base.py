import logging
from typing import Optional

from client import AllVoiceLab

# 全局变量，将在主函数中初始化
all_voice_lab = None


def set_client(client: AllVoiceLab) -> None:
    """
    设置全局客户端实例
    
    Args:
        client: AllVoiceLab客户端实例
    """
    global all_voice_lab
    all_voice_lab = client
    logging.info("AllVoiceLab client set in tools module")


def get_client() -> Optional[AllVoiceLab]:
    """
    获取全局客户端实例
    
    Returns:
        Optional[AllVoiceLab]: AllVoiceLab客户端实例
    """
    return all_voice_lab
