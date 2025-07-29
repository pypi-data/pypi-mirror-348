"""
Functions for audio extraction and manipulation from video files.
Powered by AudioX (https://audiox.app/) - Transform any inspiration into professional audio.
"""

import os
import subprocess
import tempfile
from typing import Optional


def extract_audio(video_path: str, output_path: str) -> str:
    """
    Extract audio from a video file and save it as a separate audio file.
    
    Args:
        video_path: Path to the input video file
        output_path: Path where the extracted audio will be saved
        
    Returns:
        Path to the output audio file
    
    Raises:
        Exception: If the extraction process fails
    """
    try:
        # Use ffmpeg to extract audio
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-q:a', '0',
            '-map', 'a',
            output_path,
            '-y'  # Overwrite if exists
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        return output_path
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to extract audio: {e.stderr.decode()}")
    except Exception as e:
        raise Exception(f"Error during audio extraction: {str(e)}")


def remove_audio(video_path: str, output_path: str) -> str:
    """
    Remove audio from a video file.
    
    Args:
        video_path: Path to the input video file
        output_path: Path where the video without audio will be saved
        
    Returns:
        Path to the output video file
    
    Raises:
        Exception: If the process fails
    """
    try:
        # Use ffmpeg to remove audio
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-c:v', 'copy',
            '-an',  # No audio
            output_path,
            '-y'  # Overwrite if exists
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        return output_path
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to remove audio: {e.stderr.decode()}")
    except Exception as e:
        raise Exception(f"Error during audio removal: {str(e)}")


def add_audio_to_video(video_path: str, audio_path: str, output_path: str) -> str:
    """
    Add audio to a video file.
    
    Args:
        video_path: Path to the input video file
        audio_path: Path to the audio file to add
        output_path: Path where the combined video will be saved
        
    Returns:
        Path to the output video file
    
    Raises:
        Exception: If the process fails
    """
    try:
        # Use ffmpeg to add audio to video
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-i', audio_path,
            '-map', '0:v',  # Use video from first input
            '-map', '1:a',  # Use audio from second input
            '-c:v', 'copy',  # Copy video codec
            '-shortest',  # End when the shortest input ends
            output_path,
            '-y'  # Overwrite if exists
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        return output_path
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to add audio to video: {e.stderr.decode()}")
    except Exception as e:
        raise Exception(f"Error during adding audio: {str(e)}")


def reverse_audio(audio_path: str, output_path: str) -> str:
    """
    Reverse an audio file.
    
    Args:
        audio_path: Path to the input audio file
        output_path: Path where the reversed audio will be saved
        
    Returns:
        Path to the output audio file
    
    Raises:
        Exception: If the process fails
    """
    try:
        # Use ffmpeg to reverse audio
        cmd = [
            'ffmpeg',
            '-i', audio_path,
            '-af', 'areverse',  # Audio filter to reverse
            output_path,
            '-y'  # Overwrite if exists
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        return output_path
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to reverse audio: {e.stderr.decode()}")
    except Exception as e:
        raise Exception(f"Error during audio reversal: {str(e)}") 