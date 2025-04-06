from app.utils.ffmpeg.base import run_ffmpeg_command

# Advanced Editing  

def detect_silence(audio_path: str):
    """
    Detect silence in an audio file.

    Args:
        audio_path (str): Path to the input audio file.

    This function runs an FFmpeg command that detects periods of silence in the audio.
    - The `-af silencedetect=noise=-30dB:d=2` argument specifies the silence detection filter:
        - `noise=-30dB`: The noise threshold for detecting silence (anything below -30dB is considered silence).
        - `d=2`: The duration of silence in seconds to be detected.
    - The `-f null -` argument tells FFmpeg to process the audio but not output a file (since we're just detecting the silence).
    """
    command = f"ffmpeg -i {audio_path} -af silencedetect=noise=-30dB:d=2 -f null -"
    run_ffmpeg_command(command)

def detect_scene_changes(video_path: str):
    """
    Detect scene changes in a video file.

    Args:
        video_path (str): Path to the input video file.

    This function runs an FFmpeg command that detects scene changes based on pixel differences.
    - The `-vf "select='gt(scene,0.3)',showinfo"` argument applies a video filter:
        - `select='gt(scene,0.3)'`: Selects frames where the scene change is greater than 0.3 (a threshold for detecting changes).
        - `showinfo`: Displays information about the selected frames (scene changes).
    - The `-vsync vfr` argument forces variable frame rate output, allowing FFmpeg to handle frames that are not evenly spaced.
    - The `frames_%04d.png` output name pattern saves each detected frame as an image (e.g., `frames_0001.png`, `frames_0002.png`, etc.).
    """
    command = f"ffmpeg -i {video_path} -vf \"select='gt(scene,0.3)',showinfo\" -vsync vfr frames_%04d.png"
    run_ffmpeg_command(command)
