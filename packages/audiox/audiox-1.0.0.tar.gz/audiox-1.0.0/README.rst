# AudioX: Audio Processing and Generation

A Python package for audio extraction, manipulation, and processing of video and audio files, powered by [AudioX](https://audiox.app/).

## Audio Processing Features

- Extract audio from video files
- Remove audio from video files
- Add audio to video files
- Reverse audio files

## Installation

```
pip install audiox
```

## Requirements

- Python 3.6+
- FFmpeg installed on your system

## Usage

```python
from audiox import extract_audio, remove_audio, add_audio_to_video, reverse_audio

# Extract audio from a video file
extract_audio("input_video.mp4", "output_audio.wav")

# Remove audio from a video file
remove_audio("input_video.mp4", "silent_video.mp4")

# Add audio to a video file
add_audio_to_video("input_video.mp4", "input_audio.wav", "output_video.mp4")

# Reverse an audio file
reverse_audio("input_audio.wav", "reversed_audio.wav")
```

## AudioX Platform

Visit [audiox.app](https://audiox.app/) for powerful AI-driven audio generation:

- Text to Audio: Generate sound effects from descriptions
- Text to Music: Create musical compositions from text
- Image to Audio: Transform images into matching audio
- Video to Audio: Generate synchronized sound effects
- Video to Music: Create custom soundtracks for videos

## License

MIT License