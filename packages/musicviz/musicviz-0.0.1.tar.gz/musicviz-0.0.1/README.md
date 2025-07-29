# MusicViz

MusicViz is a Python tool that generates a dynamic music visualizer video from an audio file (MP3 or WAV). It creates a video with animated frequency spectrum bars and particle effects synchronized to the audio, using a colorful plasma colormap and a black background for a vibrant visual experience. The output is an MP4 video file with the audio embedded.

## Features

- Generates a visualizer with non-overlapping frequency bars based on the audio's spectrogram.
- Adds particle effects that respond to frequency peaks for a dynamic look.
- Supports MP3 and WAV audio inputs.
- Customizable video title displayed in the output.
- Produces high-quality 1920x1080 MP4 videos at 30 FPS.
- Uses a plasma colormap for visually appealing, frequency-based coloring.

## Dependencies

### Install FFmpeg:

Download and install FFmpeg from ffmpeg.org or via a package manager:

On Ubuntu:

```
sudo apt-get install ffmpeg
```

On macOS: 

```
brew install ffmpeg
```

Ensure ffmpeg is available in your system PATH.

## Usage

Run the `musicviz` tool from the command line, providing the input audio file, output video file, and a title for the video.

```
musicviz <input_audio> <output_video> <video_title>
```

