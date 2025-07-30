# -*- coding: utf-8 -*-
"""
Video to Audio Converter 视频转音频工具
@Auth ： dny
@Time ： 2025-05-16 21:04
"""

from pathlib import Path
from typing import Optional
from moviepy.editor import AudioFileClip

# Supported audio output formats 支持的音频输出格式
SUPPORTED_FORMATS = ["wav", "mp3", "ogg", "aac", "m4a"]


def convert_video_to_audio(
        video_file_path: str,
        output_audio_path: Optional[str] = None,
        output_format: str = "wav",
        codec: Optional[str] = None,
        bitrate: Optional[str] = None,
        verbose: bool = True,
) -> str:
    """
    Convert video file to audio file / 将视频文件转换为音频文件

    Args / 参数:
        video_file_path (str): Input video file path / 输入视频文件路径
        output_audio_path (Optional[str]): Output audio file path / 输出音频文件路径
        output_format (str): Output audio format (default: "wav") / 输出音频格式(默认wav)
        codec (Optional[str]): Audio codec / 音频编码器
        bitrate (Optional[str]): Audio bitrate / 音频比特率
        verbose (bool): Show conversion progress (default: True) / 显示转换进度(默认显示)

    Returns / 返回:
        str: Path to the output audio file / 输出音频文件路径

    Raises / 异常:
        FileNotFoundError: When input video doesn't exist / 输入视频不存在时抛出
        ValueError: When output format is not supported / 输出格式不支持时抛出
        RuntimeError: When audio conversion fails / 音频转换失败时抛出
    """
    # Convert input path to Path object / 将输入路径转为Path对象
    video_path = Path(video_file_path)

    # Check if input file exists / 检查输入文件是否存在
    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_file_path}")

    # Check if output format is supported / 检查输出格式是否支持
    if output_format.lower() not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported output format: {output_format}. "
            f"Supported formats: {', '.join(SUPPORTED_FORMATS)}"
        )

    # If output path not specified, use same path with new extension
    # 如果未指定输出路径，则使用相同路径但修改扩展名
    if output_audio_path is None:
        output_audio_path = str(video_path.with_suffix(f".{output_format}"))

    try:
        # Show conversion info if verbose=True / 如果verbose为True则显示转换信息
        if verbose:
            print(f"Converting {video_file_path} to audio...")

        # Load audio from video file using moviepy / 使用moviepy加载视频中的音频
        audio_clip = AudioFileClip(video_file_path)

        # Write audio to file / 将音频写入文件
        audio_clip.write_audiofile(
            output_audio_path,
            codec=codec,  # Audio codec / 音频编码器
            bitrate=bitrate,  # Bitrate / 比特率
            logger="bar" if verbose else None  # Show progress bar if verbose / 根据verbose显示进度条
        )

        # Show completion info if verbose=True / 如果verbose为True则显示完成信息
        if verbose:
            print(f"Successfully saved audio to: {output_audio_path}")

        return output_audio_path
    except Exception as e:
        # Catch and re-raise conversion errors / 捕获并重新抛出转换异常
        raise RuntimeError(f"Audio conversion failed: {str(e)}")
    finally:
        # Make sure to close audio clip / 确保关闭音频剪辑对象
        if 'audio_clip' in locals():
            audio_clip.close()