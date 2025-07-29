"""
audiox: A Python package for audio processing.

This package provides utilities for audio extraction, manipulation, and processing.
Powered by AudioX (https://audiox.app/) - Transform any inspiration into professional audio.
"""

from .extract_audio import extract_audio, remove_audio, add_audio_to_video, reverse_audio

__all__ = ['extract_audio', 'remove_audio', 'add_audio_to_video', 'reverse_audio']

__version__ = '1.0.0'
__author__ = 'GaoQ1'
__email__ = 'gaoquan199035@gmail.com'
__url__ = 'https://audiox.app/' 