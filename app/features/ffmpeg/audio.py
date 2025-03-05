from app.features.ffmpeg.base import run_ffmpeg_command

# Audio Processing Functions

def extract_audio(video_path: str, output_audio_path: str):
    """
    Extract audio from a video file.

    Args:
        video_path (str): Path to the input video file.
        output_audio_path (str): Path where the extracted audio will be saved.

    This function uses FFmpeg to extract the audio stream from a video and save it to a specified file.
    - `-q:a 0` ensures the audio extraction is of the best possible quality.
    - `-map a` maps the audio stream to the output file.
    """
    command = f"ffmpeg -i {video_path} -q:a 0 -map a {output_audio_path}"
    run_ffmpeg_command(command)

def merge_audio_files(audio_list: list, output_audio_path: str):
    """
    Merge multiple audio files into a single audio file.

    Args:
        audio_list (list): List of audio file paths to be merged.
        output_audio_path (str): Path where the merged audio will be saved.

    This function writes the paths of the audio files to a temporary text file (`audio_list.txt`), which is then used by FFmpeg to concatenate the audio files.
    - `-f concat` tells FFmpeg to concatenate the audio files.
    - `-safe 0` allows FFmpeg to handle file paths that may include special characters.
    - `-c copy` performs the merging without re-encoding the audio, preserving the original quality.
    """
    with open("audio_list.txt", "w") as f:
        for audio in audio_list:
            f.write(f"file '{audio}'\n")
    command = f"ffmpeg -f concat -safe 0 -i audio_list.txt -c copy {output_audio_path}"
    run_ffmpeg_command(command)

def change_audio_speed(audio_path: str, speed: float, output_path: str):
    """
    Change the speed of an audio file.

    Args:
        audio_path (str): Path to the input audio file.
        speed (float): Factor by which to change the speed (e.g., 1.5 for 50% faster, 0.5 for 50% slower).
        output_path (str): Path where the modified audio will be saved.

    This function uses FFmpeg's `atempo` filter to change the speed of the audio. 
    - The `atempo` filter allows a range of values between 0.5 and 2.0 for speed adjustments.
    """
    command = f"ffmpeg -i {audio_path} -filter:a \"atempo={speed}\" {output_path}"
    run_ffmpeg_command(command)

def adjust_audio_volume(audio_path: str, volume: float, output_path: str):
    """
    Adjust the volume of an audio file.

    Args:
        audio_path (str): Path to the input audio file.
        volume (float): Factor by which to change the volume (e.g., 1.0 for no change, 2.0 for double the volume).
        output_path (str): Path where the adjusted audio will be saved.

    This function uses FFmpeg's `volume` filter to adjust the audio volume.
    - The `volume` filter allows you to increase or decrease the volume by the specified factor.
    """
    command = f"ffmpeg -i {audio_path} -filter:a \"volume={volume}\" {output_path}"
    run_ffmpeg_command(command)
    
def normalize_audio(input_path: str, output_path: str):
    """
    Normalize the audio levels of a file.

    Args:
        input_path (str): Path to the input audio file.
        output_path (str): Path where the normalized audio will be saved.

    This function uses FFmpeg's `loudnorm` filter to normalize the audio levels so that the overall volume is consistent.
    - The `loudnorm` filter automatically adjusts the volume to meet specific loudness standards.
    """
    command = f"ffmpeg -i {input_path} -filter:a loudnorm {output_path}"
    run_ffmpeg_command(command)
