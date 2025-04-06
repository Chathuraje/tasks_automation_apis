from app.utils.ffmpeg.base import run_ffmpeg_command

# Subtitle Processing Functions

def add_subtitles(video_path: str, subtitle_path: str, output_path: str):
    """
    Add subtitles to a video.

    Args:
        video_path (str): Path to the input video file.
        subtitle_path (str): Path to the subtitle file (e.g., .srt, .ass).
        output_path (str): Path where the video with subtitles will be saved.

    This function overlays subtitles onto a video using FFmpeg.
    - `-vf "subtitles={subtitle_path}"`: Applies subtitles to the video. The `-vf` flag specifies a video filter, and this one adds the subtitles from the given file.
    """
    command = f"ffmpeg -i {video_path} -vf \"subtitles={subtitle_path}\" {output_path}"
    run_ffmpeg_command(command)
    
def add_permanent_subtitles(video_path: str, subtitle_path: str, output_path: str, style: str = None):
    """
    Hardcode subtitles into a video (permanent subtitles) with optional style and position.

    Parameters:
        video_path (str): Path to the input video file.
        subtitle_path (str): Path to the subtitle file.
        output_path (str): Path where the output video will be saved.
        style (str, optional): Subtitle style parameters (e.g., "FontName=Arial,FontSize=24,PrimaryColour=&HFFFFFF&").
        alignment (int, optional): Alignment value for subtitle positioning (e.g., 2 for bottom-center).
                                    See ASS alignment values for details.
    """
    force_style_options = []
    
    if style:
        force_style_options.append(style)
    
    # Build the subtitles filter string
    if force_style_options:
        force_style_str = ",".join(force_style_options)
        # Note: wrapping paths in quotes to handle spaces
        command = (
            f"ffmpeg -i {video_path} -vf \"subtitles={subtitle_path}:force_style='{force_style_str}'\" {output_path}"
        )
    else:
        command = f'ffmpeg -i "{video_path}" -vf "subtitles={subtitle_path}" "{output_path}"'
    
    run_ffmpeg_command(command)



def extract_subtitles(video_path: str, output_subtitle_path: str):
    """
    Extract subtitles from a video.

    Args:
        video_path (str): Path to the input video file.
        output_subtitle_path (str): Path where the extracted subtitle file will be saved.

    This function extracts subtitles from a video file and saves them in the specified format (e.g., .srt).
    - `-map 0:s:0`: Selects the subtitle stream (first subtitle stream).
    """
    command = f"ffmpeg -i {video_path} -map 0:s:0 {output_subtitle_path}"
    run_ffmpeg_command(command)


def convert_srt_to_ass(srt_path: str, ass_path: str):
    """
    Convert subtitles from SRT format to ASS format.

    Args:
        srt_path (str): Path to the input SRT subtitle file.
        ass_path (str): Path where the output ASS subtitle file will be saved.

    This function converts SRT subtitles to ASS format using FFmpeg.
    """
    command = f"ffmpeg -i {srt_path} {ass_path}"
    run_ffmpeg_command(command)