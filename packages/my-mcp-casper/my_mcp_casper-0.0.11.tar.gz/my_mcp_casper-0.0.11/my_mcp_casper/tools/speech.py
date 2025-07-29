import logging

from mcp.types import TextContent

from client.all_voice_lab import VoiceCloneNoPermissionError
from .base import get_client
from .utils import validate_audio_file, validate_output_directory, create_error_response, create_success_response


def text_to_speech(
    text: str,
    voice_id: str,
    model_id: str,
    speed: int = 1,
    output_dir: str = None
) -> TextContent:
    """
    将文本转换为语音
    
    Args:
        text: 用于语音合成的目标文本。最多5,000个字符。
        voice_id: 用于合成的语音ID。必填。必须是可用语音中的有效语音ID（使用get_voices工具获取）。
        model_id: 用于合成的模型ID。必填。必须是可用模型中的有效模型ID（使用get_models工具获取）。
        speed: 语速调整，范围[-5, 5]，其中-5最慢，5最快。默认值为1。
        output_dir: 生成的音频文件的输出目录。默认为用户的桌面。
        
    Returns:
        TextContent: 包含生成的音频文件路径的文本内容。
    """
    all_voice_lab = get_client()
    output_dir = all_voice_lab.get_output_path(output_dir)
    logging.info(f"Tool called: text_to_speech, voice_id: {voice_id}, model_id: {model_id}, speed: {speed}")
    logging.info(f"Output directory: {output_dir}")

    # Validate parameters
    if not text:
        logging.warning("Text parameter is empty")
        return TextContent(
            type="text",
            text="text parameter cannot be empty"
        )
    if len(text) > 5000:
        logging.warning(f"Text parameter exceeds maximum length: {len(text)} characters")
        return TextContent(
            type="text",
            text="text parameter cannot exceed 5,000 characters"
        )
    if not voice_id:
        logging.warning("voice_id parameter is empty")
        return TextContent(
            type="text",
            text="voice_id parameter cannot be empty"
        )
    if not model_id:
        logging.warning("model_id parameter is empty")
        return TextContent(
            type="text",
            text="model_id parameter cannot be empty"
        )

    # Validate model_id against available models
    try:
        logging.info(f"Validating model_id: {model_id}")
        model_resp = all_voice_lab.get_supported_voice_model()
        available_models = model_resp.models
        valid_model_ids = [model.model_id for model in available_models]

        if model_id not in valid_model_ids:
            logging.warning(f"Invalid model_id: {model_id}, available models: {valid_model_ids}")
            return TextContent(
                type="text",
                text=f"Invalid model_id: {model_id}. Please use a valid model ID."
            )
        logging.info(f"Model ID validation successful: {model_id}")
    except Exception as e:
        logging.error(f"Failed to validate model_id: {str(e)}")
        # Continue with the process even if validation fails
        # to maintain backward compatibility

    try:
        logging.info(f"Starting text-to-speech processing, text length: {len(text)} characters")
        file_path = all_voice_lab.text_to_speech(text, voice_id, model_id, output_dir, speed)
        logging.info(f"Text-to-speech successful, file saved at: {file_path}")
        return TextContent(
            type="text",
            text=f"Speech generation completed, file saved at: {file_path}\n"
        )
    except Exception as e:
        logging.error(f"Text-to-speech failed: {str(e)}")
        return TextContent(
            type="text",
            text=f"Synthesis failed, tool temporarily unavailable"
        )


def speech_to_speech(
    audio_file_path: str,
    voice_id: str,
    similarity: float = 1,
    remove_background_noise: bool = False,
    output_dir: str = None
) -> TextContent:
    """
    将音频转换为另一个声音，同时保留语音内容
    
    Args:
        audio_file_path: 源音频文件的路径。仅支持MP3和WAV格式。最大文件大小：50MB。
        voice_id: 用于转换的语音ID。必填。必须是可用语音中的有效语音ID（使用get_voices工具获取）。
        similarity: 语音相似度因子，范围[0, 1]，其中0最不相似，1最相似于原始语音特征。默认值为1。
        remove_background_noise: 是否在转换前从源音频中去除背景噪音。默认为False。
        output_dir: 生成的音频文件的输出目录。默认为用户的桌面。
        
    Returns:
        TextContent: 包含使用新声音生成的音频文件路径的文本内容。
    """
    all_voice_lab = get_client()
    output_dir = all_voice_lab.get_output_path(output_dir)
    logging.info(f"Tool called: speech_to_speech, voice_id: {voice_id}, similarity: {similarity}")
    logging.info(f"Audio file path: {audio_file_path}, remove background noise: {remove_background_noise}")
    logging.info(f"Output directory: {output_dir}")

    # 验证音频文件
    is_valid, error_message = validate_audio_file(audio_file_path)
    if not is_valid:
        return create_error_response(error_message)

    # 验证voice_id参数
    if not voice_id:
        logging.warning("voice_id parameter is empty")
        return create_error_response("voice_id parameter cannot be empty")

    # 验证voice_id格式（基本检查）
    if not isinstance(voice_id, str) or len(voice_id.strip()) == 0:
        logging.warning(f"Invalid voice_id format: {voice_id}")
        return create_error_response("Invalid voice_id format")

    # 验证similarity范围
    if similarity < 0 or similarity > 1:
        logging.warning(f"Similarity parameter {similarity} is out of range [0, 1]")
        return create_error_response("similarity parameter must be between 0 and 1")

    # 验证并创建输出目录
    is_valid, error_message = validate_output_directory(output_dir)
    if not is_valid:
        return create_error_response(error_message)

    try:
        logging.info("Starting speech conversion processing")
        file_path = all_voice_lab.speech_to_speech(audio_file_path, voice_id, output_dir, similarity,
                                                   remove_background_noise)
        logging.info(f"Speech conversion successful, file saved at: {file_path}")
        return create_success_response(f"Audio conversion completed, file saved at: {file_path}\n")
    except FileNotFoundError as e:
        logging.error(f"Audio file does not exist: {audio_file_path}, error: {str(e)}")
        return create_error_response(f"Audio file does not exist: {audio_file_path}")
    except Exception as e:
        logging.error(f"Speech conversion failed: {str(e)}")
        return create_error_response("Conversion failed, tool temporarily unavailable")


def isolate_human_voice(
    audio_file_path: str,
    output_dir: str = None
) -> TextContent:
    """
    通过去除背景噪音和非语音声音来提取干净的人声
    
    Args:
        audio_file_path: 要处理的音频文件的路径。仅支持MP3和WAV格式。最大文件大小：50MB。
        output_dir: 处理后的音频文件的输出目录。默认为用户的桌面。
        
    Returns:
        TextContent: 包含带有隔离人声的生成音频文件路径的文本内容。
    """
    all_voice_lab = get_client()
    output_dir = all_voice_lab.get_output_path(output_dir)
    logging.info(f"Tool called: isolate_human_voice")
    logging.info(f"Audio file path: {audio_file_path}")
    logging.info(f"Output directory: {output_dir}")

    # 验证音频文件
    is_valid, error_message = validate_audio_file(audio_file_path)
    if not is_valid:
        return create_error_response(error_message)

    # 验证并创建输出目录
    is_valid, error_message = validate_output_directory(output_dir)
    if not is_valid:
        return create_error_response(error_message)

    try:
        logging.info("Starting human voice isolation processing")
        file_path = all_voice_lab.audio_isolation(audio_file_path, output_dir)
        logging.info(f"Human voice isolation successful, file saved at: {file_path}")
        return create_success_response(f"Voice isolation completed, file saved at: {file_path}\n")
    except FileNotFoundError as e:
        logging.error(f"Audio file does not exist: {audio_file_path}, error: {str(e)}")
        return create_error_response(f"Audio file does not exist: {audio_file_path}")
    except Exception as e:
        logging.error(f"Human voice isolation failed: {str(e)}")
        return create_error_response("Voice isolation failed, tool temporarily unavailable")


def clone_voice(
    audio_file_path: str,
    name: str,
    description: str = None
) -> TextContent:
    """
    通过从音频样本克隆创建自定义语音配置文件
    
    Args:
        audio_file_path: 包含要克隆的语音样本的音频文件的路径。仅支持MP3和WAV格式。最大文件大小：10MB。
        name: 分配给克隆语音配置文件的名称。必填。
        description: 克隆语音配置文件的可选描述。
        
    Returns:
        TextContent: 包含新创建的语音配置文件的语音ID的文本内容。
    """
    all_voice_lab = get_client()
    logging.info(f"Tool called: clone_voice")
    logging.info(f"Audio file path: {audio_file_path}")
    logging.info(f"Voice name: {name}")
    if description:
        logging.info(f"Voice description: {description}")

    # 验证音频文件，使用10MB的大小限制
    is_valid, error_message = validate_audio_file(audio_file_path, max_size_mb=10)
    if not is_valid:
        return create_error_response(error_message)

    # 验证名称参数
    if not name:
        logging.warning("Name parameter is empty")
        return create_error_response("name parameter cannot be empty")

    try:
        logging.info("Starting voice cloning process")
        voice_id = all_voice_lab.add_voice(name, audio_file_path, description)
        logging.info(f"Voice cloning successful, voice ID: {voice_id}")
        return TextContent(
            type="text",
            text=f"Voice cloning completed. Your new voice ID is: {voice_id}\n"
        )
    except VoiceCloneNoPermissionError as e:
        logging.error(f"Voice cloning failed: {str(e)}")
        return TextContent(
            type="text",
            text=f"Voice cloning failed, you don't have permission to clone voice. Please contact AllVoiceLab com."
        )
    except FileNotFoundError as e:
        logging.error(f"Audio file does not exist: {audio_file_path}, error: {str(e)}")
        return TextContent(
            type="text",
            text=f"Audio file does not exist: {audio_file_path}"
        )
    except Exception as e:
        logging.error(f"Voice cloning failed: {str(e)}")
        return TextContent(
            type="text",
            text=f"Voice cloning failed, tool temporarily unavailable"
        )
