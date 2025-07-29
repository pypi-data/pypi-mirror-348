import logging
import os
import random
import time

import requests
from mcp.types import TextContent

from .base import get_client
from .utils import validate_output_directory, create_error_response


def download_dubbing_file(
    dubbing_id: str,
    output_dir: str = None
) -> TextContent:
    """
    从已完成的配音项目下载音频文件
    
    Args:
        dubbing_id: 要下载的配音项目的唯一标识符。必填。
        output_dir: 下载的音频文件的输出目录。默认为用户的桌面。
        
    Returns:
        TextContent: 包含下载的音频文件路径的文本内容。
    """
    all_voice_lab = get_client()
    output_dir = all_voice_lab.get_output_path(output_dir)
    logging.info(f"Tool called: download_dubbing_audio")
    logging.info(f"Dubbing ID: {dubbing_id}")
    logging.info(f"Output directory: {output_dir}")

    # Validate parameters
    if not dubbing_id:
        logging.warning("Dubbing ID parameter is empty")
        return TextContent(
            type="text",
            text="dubbing_id parameter cannot be empty"
        )

    # 验证并创建输出目录
    is_valid, error_message = validate_output_directory(output_dir)
    if not is_valid:
        return create_error_response(error_message)

    try:
        logging.info(f"Starting dubbing audio download, dubbing ID: {dubbing_id}")
        file_path = all_voice_lab.download_dubbing_audio(dubbing_id, output_dir)
        logging.info(f"Dubbing audio download successful, file saved at: {file_path}")
        return TextContent(
            type="text",
            text=f"Dubbing audio download completed, file saved at: {file_path}\n"
        )
    except Exception as e:
        logging.error(f"Dubbing audio download failed: {str(e)}")
        return TextContent(
            type="text",
            text=f"Download failed, tool temporarily unavailable"
        )


def remove_subtitle(
    video_file_path: str,
    language_code: str = "auto",
    name: str = None,
    output_dir: str = None
) -> TextContent:
    """
    使用OCR技术从视频中删除硬编码字幕
    
    Args:
        video_file_path: 要处理的视频文件的路径。仅支持MP4和MOV格式。最大文件大小：2GB。
        language_code: 字幕文本检测的语言代码（例如，'en'，'zh'）。设置为'auto'进行自动语言检测。默认为'auto'。
        name: 用于识别目的的可选项目名称。
        output_dir: 处理后的视频文件的输出目录。默认为用户的桌面。
        
    Returns:
        TextContent: 包含处理后的视频文件路径或错误消息的文本内容。
        如果处理时间超过预期，则返回项目ID以便稍后检查状态。
    """
    all_voice_lab = get_client()
    output_dir = all_voice_lab.get_output_path(output_dir)

    poll_interval = 10
    max_retries = 30
    logging.info(f"Tool called: subtitle_removal")
    logging.info(f"Video file path: {video_file_path}")
    logging.info(f"Language code: {language_code}")
    logging.info(f"Output directory: {output_dir}")
    logging.info(f"Poll interval: {poll_interval} seconds")
    logging.info(f"Max retries: {max_retries}")
    if name:
        logging.info(f"Project name: {name}")

    # Validate parameters
    if not video_file_path:
        logging.warning("Video file path parameter is empty")
        return TextContent(
            type="text",
            text="video_file_path parameter cannot be empty"
        )

    # Check if video file exists before processing
    if not os.path.exists(video_file_path):
        logging.warning(f"Video file does not exist: {video_file_path}")
        return TextContent(
            type="text",
            text=f"Video file does not exist: {video_file_path}"
        )

    # Check file format, only allow mp4 and mov
    _, file_extension = os.path.splitext(video_file_path)
    file_extension = file_extension.lower()
    if file_extension not in [".mp4", ".mov"]:
        logging.warning(f"Unsupported video file format: {file_extension}")
        return TextContent(
            type="text",
            text=f"Unsupported video file format. Only MP4 and MOV formats are supported."
        )

    # Check file size, limit to 2GB
    max_size_bytes = 2 * 1024 * 1024 * 1024  # 2GB in bytes
    file_size = os.path.getsize(video_file_path)
    if file_size > max_size_bytes:
        logging.warning(f"Video file size exceeds limit: {file_size} bytes, max allowed: {max_size_bytes} bytes")
        return TextContent(
            type="text",
            text=f"Video file size exceeds the maximum limit of 2GB. Please use a smaller file."
        )

    try:
        logging.info("Starting subtitle removal process")
        project_id = all_voice_lab.subtitle_removal(
            video_file_path=video_file_path,
            language_code=language_code,
            name=name
        )
        logging.info(f"Subtitle removal initiated, project ID: {project_id}")

        # Poll for task completion
        logging.info(f"Starting to poll for task completion, interval: {poll_interval}s, max retries: {max_retries}")

        # Initialize variables for polling
        retry_count = 0
        task_completed = False
        removal_info = None

        # Poll until task is completed or max retries reached
        while retry_count < max_retries and not task_completed:
            try:
                # Wait for the specified interval
                time.sleep(poll_interval)

                # Check task status
                removal_info = all_voice_lab.get_removal_info(project_id)
                logging.info(f"Poll attempt {retry_count + 1}, status: {removal_info.status}")

                # Check if task is completed
                if removal_info.status.lower() == "success":
                    task_completed = True
                    logging.info("Subtitle removal task completed successfully")
                    break
                elif removal_info.status.lower() == "failed":
                    logging.error("Subtitle removal task failed")
                    return TextContent(
                        type="text",
                        text=f"Subtitle removal failed. Please try again later."
                    )

                # Increment retry count
                retry_count += 1

            except Exception as e:
                logging.error(f"Error checking task status: {str(e)}")
                retry_count += 1

        # Check if task completed successfully
        if not task_completed:
            logging.warning(f"Subtitle removal task did not complete within {max_retries} attempts")
            return TextContent(
                type="text",
                text=f"Subtitle removal is still in progress. Your project ID is: {project_id}. You can check the status later."
            )

        # Download the processed video
        logging.info("Downloading processed video")
        try:
            # Check if output URL is available
            if not removal_info.removal_result:
                logging.error("No removal_result URL available in the response")
                return TextContent(
                    type="text",
                    text=f"Subtitle removal completed but no output file is available. Your project ID is: {project_id}"
                )

            # Prepare HTTP request
            url = removal_info.removal_result

            # Set request headers, accept all types of responses
            headers = all_voice_lab._get_headers(content_type="", accept="*/*")

            # Send request and get response
            response = requests.get(url, headers=headers, stream=True)

            # Check response status
            response.raise_for_status()

            # Generate a unique filename
            timestamp = int(time.time())
            random_suffix = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=6))
            filename = f"subtitle_removal_{timestamp}_{random_suffix}.mp4"

            # Build complete file path
            file_path = os.path.join(output_dir, filename)

            # Save response content to file
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            logging.info(f"Processed video saved to: {file_path}")
            return TextContent(
                type="text",
                text=f"Subtitle removal completed successfully. Processed video saved to: {file_path}"
            )

        except Exception as e:
            logging.error(f"Failed to download processed video: {str(e)}")
            return TextContent(
                type="text",
                text=f"Subtitle removal completed but failed to download the processed video. Your project ID is: {project_id}"
            )

    except FileNotFoundError as e:
        logging.error(f"Video file does not exist: {video_file_path}, error: {str(e)}")
        return TextContent(
            type="text",
            text=f"Video file does not exist: {video_file_path}"
        )
    except Exception as e:
        logging.error(f"Subtitle removal failed: {str(e)}")
        return TextContent(
            type="text",
            text=f"Subtitle removal failed, tool temporarily unavailable"
        )


def video_translation_dubbing(
    video_file_path: str,
    target_lang: str,
    source_lang: str = "auto",
    name: str = None,
    watermark: bool = False,
    output_dir: str = None
) -> TextContent:
    """
    将视频语音翻译并配音成不同语言，使用AI生成的声音
    
    Args:
        video_file_path: 要处理的视频或音频文件的路径。支持MP4、MOV、MP3和WAV格式。最大文件大小：2GB。
        target_lang: 翻译的目标语言代码（例如，'en'，'zh'，'ja'，'fr'，'de'，'ko'）。必填。
        source_lang: 原始内容的源语言代码。设置为'auto'进行自动语言检测。默认为'auto'。
        name: 用于识别目的的可选项目名称。
        watermark: 是否在输出视频中添加水印。默认为False。
        output_dir: 下载的结果文件的输出目录。默认为用户的桌面。
        
    Returns:
        TextContent: 包含配音ID和下载的结果文件路径的文本内容。
        如果处理时间超过预期，则仅返回配音ID以便稍后检查状态。
    """
    all_voice_lab = get_client()
    output_dir = all_voice_lab.get_output_path(output_dir)

    max_polling_time = 300
    polling_interval = 10
    logging.info(f"Tool called: video_translation_dubbing")
    logging.info(f"Video file path: {video_file_path}")
    logging.info(f"Target language: {target_lang}, Source language: {source_lang}")
    if name:
        logging.info(f"Project name: {name}")
    logging.info(f"Watermark: {watermark}")
    logging.info(f"Output directory: {output_dir}")
    logging.info(f"Max polling time: {max_polling_time}s, Polling interval: {polling_interval}s")

    # Validate parameters
    if not video_file_path:
        logging.warning("Video file path parameter is empty")
        return TextContent(
            type="text",
            text="video_file_path parameter cannot be empty"
        )

    # Check if video file exists before processing
    if not os.path.exists(video_file_path):
        logging.warning(f"Video file does not exist: {video_file_path}")
        return TextContent(
            type="text",
            text=f"Video file does not exist: {video_file_path}"
        )

    # Check file format, only allow mp4 and mov
    _, file_extension = os.path.splitext(video_file_path)
    file_extension = file_extension.lower()
    if file_extension not in [".mp4", ".mov", ".mp3", ".wav"]:
        logging.warning(f"Unsupported video file format: {file_extension}")
        return TextContent(
            type="text",
            text=f"Unsupported video file format. Only MP4, MOV, MP3 and WAV formats are supported."
        )

    # Check file size, limit to 2GB
    max_size_bytes = 2 * 1024 * 1024 * 1024  # 2GB in bytes
    file_size = os.path.getsize(video_file_path)
    if file_size > max_size_bytes:
        logging.warning(f"Video file size exceeds limit: {file_size} bytes, max allowed: {max_size_bytes} bytes")
        return TextContent(
            type="text",
            text=f"Video file size exceeds the maximum limit of 2GB. Please use a smaller file."
        )

    # Validate target language
    if not target_lang:
        logging.warning(f"target language is empty")
        return TextContent(
            type="text",
            text="target language parameter cannot be empty"
        )

    # Validate output directory
    if not output_dir:
        logging.warning("Output directory parameter is empty")
        return TextContent(
            type="text",
            text="output_dir parameter cannot be empty"
        )

    # Try to create output directory if it doesn't exist
    try:
        os.makedirs(output_dir, exist_ok=True)
    except Exception as e:
        logging.error(f"Failed to create output directory: {output_dir}, error: {str(e)}")
        return TextContent(
            type="text",
            text=f"Failed to create output directory: {output_dir}"
        )

    try:
        # Submit dubbing request
        logging.info("Starting video dubbing process")
        dubbing_id = all_voice_lab.dubbing(
            video_file_path=video_file_path,
            target_lang=target_lang,
            source_lang=source_lang,
            name=name,
            watermark=watermark,
            drop_background_audio=False
        )
        logging.info(f"Video dubbing request successful, dubbing ID: {dubbing_id}")

        # Start polling for task completion
        logging.info(f"Starting to poll dubbing status for ID: {dubbing_id}")
        start_time = time.time()
        completed = False
        file_path = None

        # Poll until task is completed or timeout
        while time.time() - start_time < max_polling_time:
            try:
                # Get dubbing info
                dubbing_info = all_voice_lab.get_dubbing_info(dubbing_id)
                logging.info(f"Dubbing status: {dubbing_info.status} for ID: {dubbing_id}")

                # Check if dubbing is completed
                if dubbing_info.status.lower() == "success":
                    logging.info(f"Dubbing completed for ID: {dubbing_id}")
                    completed = True
                    break
                # Check if dubbing failed
                elif dubbing_info.status.lower() in ["failed", "error"]:
                    logging.error(f"Dubbing failed for ID: {dubbing_id}")
                    return TextContent(
                        type="text",
                        text=f"Video dubbing failed. Please try again later.\n"
                             f"Dubbing ID: {dubbing_id}\n"
                    )

                # Wait for next polling interval
                logging.info(f"Waiting {polling_interval} seconds before next poll")
                time.sleep(polling_interval)
            except Exception as e:
                logging.error(f"Error polling dubbing status: {str(e)}")
                time.sleep(polling_interval)  # Continue polling despite errors

        # Check if polling timed out
        if not completed:
            logging.warning(f"Polling timed out after {max_polling_time} seconds for dubbing ID: {dubbing_id}")
            return TextContent(
                type="text",
                text=f"Video dubbing is still in progress. Your dubbing ID is: {dubbing_id}\n"
                     f"The process is taking longer than expected. You can check the status later using this ID.\n"
            )

        # Download the file if dubbing completed
        try:
            logging.info(f"Downloading dubbing audio for ID: {dubbing_id}")
            file_path = all_voice_lab.get_dubbing_audio(dubbing_id, output_dir)
            logging.info(f"Dubbing audio downloaded successfully, file saved at: {file_path}")

            return TextContent(
                type="text",
                text=f"Video dubbing completed successfully!\n"
                     f"Dubbing ID: {dubbing_id}\n"
                     f"File saved at: {file_path}\n"
            )
        except Exception as e:
            logging.error(f"Failed to download dubbing audio: {str(e)}")
            return TextContent(
                type="text",
                text=f"Video dubbing completed, but failed to download the audio file.\n"
                     f"Dubbing ID: {dubbing_id}\n"
                     f"Error: {str(e)}\n"
            )
    except FileNotFoundError as e:
        logging.error(f"Video file does not exist: {video_file_path}, error: {str(e)}")
        return TextContent(
            type="text",
            text=f"Video file does not exist: {video_file_path}"
        )
    except Exception as e:
        logging.error(f"Video dubbing failed: {str(e)}")
        return TextContent(
            type="text",
            text=f"Video dubbing failed, tool temporarily unavailable"
        )


def get_dubbing_info(dubbing_id: str) -> TextContent:
    """
    检索视频配音任务的状态和详细信息
    
    Args:
        dubbing_id: 要检查的配音任务的唯一标识符。此ID由video_dubbing或video_translation_dubbing工具返回。必填。
        
    Returns:
        TextContent: 包含配音任务的状态（例如，"pending"，"processing"，"success"，"failed"）和其他详细信息的文本内容。
    """
    all_voice_lab = get_client()
    logging.info(f"Tool called: get_dubbing_info")
    logging.info(f"Dubbing ID: {dubbing_id}")

    # Validate parameters
    if not dubbing_id:
        logging.warning("Dubbing ID parameter is empty")
        return TextContent(
            type="text",
            text="dubbing_id parameter cannot be empty"
        )

    try:
        logging.info("Getting dubbing task information")
        dubbing_info = all_voice_lab.get_dubbing_info(dubbing_id)
        logging.info(f"Dubbing info retrieved successfully for ID: {dubbing_id}")

        # Format the result
        buffer = []
        buffer.append(f"Dubbing ID: {dubbing_info.dubbing_id}\n")
        buffer.append(f"Status: {dubbing_info.status}\n")

        if dubbing_info.name:
            buffer.append(f"Project Name: {dubbing_info.name}\n")
        buffer.append(
            "Note: If the task has not been completed, you may need to explicitly inform the user of the task ID when responding.\n")

        # Join the list into a string
        result = "".join(buffer)
        return TextContent(
            type="text",
            text=result
        )
    except Exception as e:
        logging.error(f"Failed to get dubbing information: {str(e)}")
        return TextContent(
            type="text",
            text=f"Failed to get dubbing information, tool temporarily unavailable"
        )


def get_removal_info(project_id: str) -> TextContent:
    """
    检索字幕移除任务的状态和详细信息
    
    Args:
        project_id: 要检查的字幕移除任务的唯一标识符。此ID由remove_subtitle工具返回。必填。
        
    Returns:
        TextContent: 包含字幕移除任务的状态（例如，"pending"，"processing"，"success"，"failed"）和其他详细信息的文本内容，
        如果任务已成功完成，则包括处理后视频的URL。
    """
    all_voice_lab = get_client()
    logging.info(f"Tool called: get_removal_info")
    logging.info(f"Project ID: {project_id}")

    # Validate parameters
    if not project_id:
        logging.warning("Project ID parameter is empty")
        return TextContent(
            type="text",
            text="project_id parameter cannot be empty"
        )

    try:
        logging.info("Getting subtitle removal task information")
        removal_info = all_voice_lab.get_removal_info(project_id)
        logging.info(f"Subtitle removal info retrieved successfully for ID: {project_id}")

        # Format the result
        buffer = []
        buffer.append(f"Project ID: {removal_info.project_id}\n")
        buffer.append(f"Status: {removal_info.status}\n")

        if removal_info.name:
            buffer.append(f"Project Name: {removal_info.name}\n")

        if removal_info.output_url and removal_info.status == "done":
            buffer.append(f"Output URL: {removal_info.output_url}\n")
            buffer.append(
                f"The subtitle removal task has been completed. You can download the processed video from the output URL.\n")
        else:
            buffer.append(
                f"The subtitle removal task is still in progress. Please check again later using the project ID.\n")

        # Join the list into a string
        result = "".join(buffer)
        return TextContent(
            type="text",
            text=result
        )
    except Exception as e:
        logging.error(f"Failed to get subtitle removal information: {str(e)}")
        return TextContent(
            type="text",
            text=f"Failed to get subtitle removal information, tool temporarily unavailable"
        )
