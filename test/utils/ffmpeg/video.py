from app.utils.ffmpeg.base import run_ffmpeg_command

# Video Processing Functions

def merge_audio_video(video_path: str, audio_path: str, output_path: str, loop=False):
    """
    Merge an audio file with a video file.

    Args:
        video_path (str): Path to the input video file.
        audio_path (str): Path to the input audio file.
        output_path (str): Path where the merged video will be saved.

    This function combines a video and an audio file into one video file, keeping the video intact and 
    encoding the audio into AAC format.
    - `-c:v copy`: Copies the video codec without re-encoding.
    - `-c:a aac`: Encodes the audio using the AAC codec.
    """
    command = f"ffmpeg -stream_loop -1  -i {video_path} -i {audio_path} -c:v copy -c:a aac -shortest {output_path}"
    run_ffmpeg_command(command)

def merge_audio_video(video_path: str, audio_path: str, output_path: str, loop: bool = False):
    """
    Merge an audio file with a video file, optionally repeating the video until the audio ends.

    Args:
        video_path (str): Path to the input video file.
        audio_path (str): Path to the input audio file.
        output_path (str): Path where the merged video will be saved.
        loop (bool): Whether to loop the video until the audio ends. Default is False.

    This function combines a video and an audio file into one video file, repeating the video until the 
    audio ends if `loop` is True, and encoding the audio into AAC format.
    - `-c:v copy`: Copies the video codec without re-encoding.
    - `-c:a aac`: Encodes the audio using the AAC codec.
    - `-stream_loop -1`: Loops the video if `loop` is True.
    - `-shortest`: Ensures the output file ends when the shortest stream (audio) finishes.
    """
    if loop:
        command = f"ffmpeg -stream_loop -1 -i {video_path} -i {audio_path} -c:v copy -c:a aac -shortest {output_path}"
    else:
        command = f"ffmpeg -i {video_path} -i {audio_path} -c:v copy -c:a aac -shortest {output_path}"

    run_ffmpeg_command(command)


def trim_video(video_path: str, start_time: str, end_time: str, output_path: str):
    """
    Trim a video from the start time to the end time.

    Args:
        video_path (str): Path to the input video file.
        start_time (str): Start time in the format `hh:mm:ss`.
        end_time (str): End time in the format `hh:mm:ss`.
        output_path (str): Path where the trimmed video will be saved.

    This function trims the video to the specified time range.
    - `-ss {start_time}`: Sets the start time of the video.
    - `-to {end_time}`: Sets the end time of the video.
    """
    command = f"ffmpeg -i {video_path} -ss {start_time} -to {end_time} -c copy {output_path}"
    run_ffmpeg_command(command)

def convert_video_format(video_path: str, output_path: str, format: str):
    """
    Convert a video to a different format.

    Args:
        video_path (str): Path to the input video file.
        output_path (str): Path where the converted video will be saved.
        format (str): The desired video format (e.g., "mp4", "avi", "mkv").

    This function converts a video file to the specified format.
    - The format is determined by the extension of `output_path`.
    """
    command = f"ffmpeg -i {video_path} {output_path}.{format}"
    run_ffmpeg_command(command)

def change_video_resolution(video_path: str, width: int, height: int, output_path: str):
    """
    Change the resolution of a video.

    Args:
        video_path (str): Path to the input video file.
        width (int): The new width for the video.
        height (int): The new height for the video.
        output_path (str): Path where the resized video will be saved.

    This function resizes the video to the specified resolution.
    - `-vf scale={width}:{height}`: Applies a video filter to change the resolution.
    """
    command = f"ffmpeg -i {video_path} -vf scale={width}:{height} {output_path}"
    run_ffmpeg_command(command)

def change_video_fps(video_path: str, fps: int, output_path: str):
    """
    Change the frame rate of a video.

    Args:
        video_path (str): Path to the input video file.
        fps (int): The new frame rate for the video.
        output_path (str): Path where the video with new frame rate will be saved.

    This function changes the frame rate of a video.
    - `-r {fps}`: Sets the new frame rate for the video.
    """
    command = f"ffmpeg -i {video_path} -r {fps} {output_path}"
    run_ffmpeg_command(command)

def add_watermark(video_path: str, watermark_path: str, output_path: str):
    """
    Add a watermark to a video.

    Args:
        video_path (str): Path to the input video file.
        watermark_path (str): Path to the watermark image file.
        output_path (str): Path where the watermarked video will be saved.

    This function overlays a watermark onto a video.
    - `-filter_complex "overlay=10:10"`: Places the watermark at the specified position (10, 10 pixels).
    """
    command = f"ffmpeg -i {video_path} -i {watermark_path} -filter_complex \"overlay=10:10\" {output_path}"
    run_ffmpeg_command(command)

def create_video_from_images(image_dir: str, output_path: str, framerate: int = 30):
    """
    Create a video from a sequence of images.

    Args:
        image_dir (str): Directory containing the image sequence.
        output_path (str): Path where the resulting video will be saved.
        framerate (int): Frame rate of the video (default is 30 FPS).

    This function creates a video by using a sequence of images in the specified directory.
    - `-pattern_type glob`: Allows the use of wildcards for file matching.
    - `-i '{image_dir}/*.png'`: Specifies the image files (e.g., PNG files).
    """
    command = f"ffmpeg -framerate {framerate} -pattern_type glob -i '{image_dir}/*.png' -c:v libx264 -pix_fmt yuv420p {output_path}"
    run_ffmpeg_command(command)

def extract_frames_from_video(input_path: str, output_dir: str):
    """
    Extract frames from a video at 1-second intervals.

    Args:
        input_path (str): Path to the input video file.
        output_dir (str): Directory where the frames will be saved.

    This function extracts frames from a video at 1-second intervals and saves them as images.
    - `-vf fps=1`: Extracts 1 frame per second.
    """
    command = f"ffmpeg -i {input_path} -vf fps=1 {output_dir}/frame_%04d.png"
    run_ffmpeg_command(command)
