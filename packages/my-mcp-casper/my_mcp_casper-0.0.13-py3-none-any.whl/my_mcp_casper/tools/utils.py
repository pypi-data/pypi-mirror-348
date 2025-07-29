import logging
import os
from typing import Tuple, Optional, List, Dict, Any

from mcp.types import TextContent

# 常量定义
AUDIO_FORMATS = [".mp3", ".wav"]


def validate_output_directory(output_dir: str) -> Tuple[bool, Optional[str]]:
    """
    验证并创建输出目录
    
    Args:
        output_dir: 输出目录路径
        
    Returns:
        Tuple[bool, Optional[str]]: (是否成功, 错误信息)
    """
    if not output_dir:
        logging.warning("Output directory parameter is empty")
        return False, "output_dir parameter cannot be empty"
        
    try:
        os.makedirs(output_dir, exist_ok=True)
        return True, None
    except Exception as e:
        logging.error(f"Failed to create output directory: {output_dir}, error: {str(e)}")
        return False, f"Failed to create output directory: {output_dir}"


def validate_audio_file(
    audio_file_path: str, 
    allowed_formats: List[str] = None,
    max_size_mb: int = 50
) -> Tuple[bool, Optional[str]]:
    """
    验证音频文件是否存在、格式是否支持、大小是否在限制范围内
    
    Args:
        audio_file_path: 音频文件路径
        allowed_formats: 允许的文件格式列表，默认为 ['.mp3', '.wav']
        max_size_mb: 最大文件大小（MB），默认为50MB
        
    Returns:
        Tuple[bool, Optional[str]]: (是否成功, 错误信息)
    """
    if allowed_formats is None:
        allowed_formats = AUDIO_FORMATS
        
    # 检查参数是否为空
    if not audio_file_path:
        logging.warning("Audio file path parameter is empty")
        return False, "audio_file_path parameter cannot be empty"
    
    # 检查文件是否存在
    if not os.path.exists(audio_file_path):
        logging.warning(f"Audio file does not exist: {audio_file_path}")
        return False, f"Audio file does not exist: {audio_file_path}"
    
    # 检查文件格式
    _, file_extension = os.path.splitext(audio_file_path)
    file_extension = file_extension.lower()
    if file_extension not in allowed_formats:
        formats_str = ", ".join(allowed_formats)
        logging.warning(f"Unsupported audio file format: {file_extension}")
        return False, f"Unsupported audio file format. Only {formats_str} formats are supported."
    
    # 检查文件大小
    max_size_bytes = max_size_mb * 1024 * 1024
    file_size = os.path.getsize(audio_file_path)
    if file_size > max_size_bytes:
        logging.warning(f"Audio file size exceeds limit: {file_size} bytes, max allowed: {max_size_bytes} bytes")
        return False, f"Audio file size exceeds the maximum limit of {max_size_mb}MB. Please use a smaller file."
    
    return True, None


def format_list_with_separator(items: List[Dict[str, Any]], key_mapping: Dict[str, str]) -> str:
    """
    使用分隔符格式化列表项
    
    Args:
        items: 要格式化的项目列表
        key_mapping: 键映射，格式为 {原始键: 显示名称}
        
    Returns:
        str: 格式化后的字符串
    """
    buffer = []
    
    for i, item in enumerate(items):
        # 如果不是第一项，添加分隔符
        if i > 0:
            buffer.append("---------------------\n")
        
        # 添加每个映射的键值对
        for original_key, display_name in key_mapping.items():
            if original_key in item.__dict__:
                buffer.append(f"- {display_name}: {getattr(item, original_key)}\n")
        
        # 处理特殊情况，如标签
        if hasattr(item, 'labels') and isinstance(item.labels, dict):
            for label_key, label_value in item.labels.items():
                # 首字母大写显示标签名称
                buffer.append(f"- {label_key.capitalize()}: {label_value}\n")
    
    # 添加最终分隔符
    buffer.append("---------------------\n")
    
    # 将列表连接成字符串
    return "".join(buffer)


def create_error_response(error_message: str) -> TextContent:
    """
    创建标准错误响应
    
    Args:
        error_message: 错误消息
        
    Returns:
        TextContent: 包含错误消息的响应
    """
    return TextContent(
        type="text",
        text=error_message
    )


def create_success_response(message: str) -> TextContent:
    """
    创建标准成功响应
    
    Args:
        message: 成功消息
        
    Returns:
        TextContent: 包含成功消息的响应
    """
    return TextContent(
        type="text",
        text=message
    )