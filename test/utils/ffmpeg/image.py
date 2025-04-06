from app.utils.ffmpeg.base import run_ffmpeg_command

# Image Processing Functions

def extract_frames(video_path: str, output_pattern: str):
    """
    Extract frames from a video file.

    Args:
        video_path (str): Path to the input video file.
        output_pattern (str): Pattern for saving the extracted frames (e.g., 'frames_%04d.png').

    This function uses FFmpeg to extract frames from a video. The frames are saved at a rate of 1 frame per second.
    - `-vf fps=1` tells FFmpeg to extract one frame every second.
    """
    command = f"ffmpeg -i {video_path} -vf fps=1 {output_pattern}"
    run_ffmpeg_command(command)

def create_gif_from_video(video_path: str, output_gif: str):
    """
    Create a GIF from a video file.

    Args:
        video_path (str): Path to the input video file.
        output_gif (str): Path where the resulting GIF will be saved.

    This function uses FFmpeg to create a GIF from the video. The video is processed with a frame rate of 10 FPS, 
    and the image is scaled to 500 pixels in width, maintaining the aspect ratio.
    - `fps=10`: Creates 10 frames per second for the GIF.
    - `scale=500:-1`: Scales the width of the video to 500 pixels while maintaining the aspect ratio.
    """
    command = f"ffmpeg -i {video_path} -vf \"fps=10,scale=500:-1\" {output_gif}"
    run_ffmpeg_command(command)
    
def convert_image_format(input_path: str, output_path: str):
    """
    Convert an image from one format to another.

    Args:
        input_path (str): Path to the input image file.
        output_path (str): Path where the converted image will be saved.

    This function uses FFmpeg to convert an image to a different format (e.g., JPG to PNG, PNG to BMP, etc.).
    - The input format is automatically determined based on the file extension, and the output format is determined by the extension of `output_path`.
    """
    command = f"ffmpeg -i {input_path} {output_path}"
    run_ffmpeg_command(command)
