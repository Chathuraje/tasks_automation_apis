from app.utils.ffmpeg.base import run_ffmpeg_command

# Streaming Functions

def stream_to_rtmp(video_path: str, rtmp_url: str):
    """
    Stream a video to an RTMP server.

    Args:
        video_path (str): Path to the input video file.
        rtmp_url (str): URL of the RTMP server where the stream will be sent.

    This function streams a video to an RTMP server using FFmpeg.
    - `-re`: Reads the input at native frame rate (real-time streaming).
    - `-c:v libx264`: Uses the H.264 codec for video encoding.
    - `-preset fast`: Sets the encoding preset to "fast" (for a good balance of speed and quality).
    - `-b:v 3000k`: Sets the video bit rate to 3000 kbps.
    - `-maxrate 3000k -bufsize 6000k`: Controls the maximum bit rate and buffer size to prevent buffering issues.
    - `-c:a aac`: Uses the AAC codec for audio encoding.
    - `-b:a 160k`: Sets the audio bit rate to 160 kbps.
    - `-f flv`: Specifies the FLV format for RTMP streaming.
    """
    command = f"ffmpeg -re -i {video_path} -c:v libx264 -preset fast -b:v 3000k -maxrate 3000k -bufsize 6000k -c:a aac -b:a 160k -f flv {rtmp_url}"
    run_ffmpeg_command(command)

def stream_to_hls(video_path: str, hls_path: str):
    """
    Stream a video to HLS format.

    Args:
        video_path (str): Path to the input video file.
        hls_path (str): Path where the HLS (HTTP Live Streaming) playlist and segments will be saved.

    This function streams a video to HLS format, which creates a series of video segments and an index playlist.
    - `-c:v libx264`: Uses the H.264 codec for video encoding.
    - `-preset veryfast`: Sets the encoding preset to "veryfast" (optimized for streaming).
    - `-crf 23`: Sets the constant rate factor for video quality (lower values = higher quality).
    - `-c:a aac`: Uses the AAC codec for audio encoding.
    - `-b:a 128k`: Sets the audio bit rate to 128 kbps.
    - `-hls_time 10`: Sets the duration of each video segment to 10 seconds.
    - `-hls_list_size 0`: Disables the playlist size limit (all segments are included in the playlist).
    - `-f hls`: Specifies the HLS output format.
    """
    command = f"ffmpeg -i {video_path} -c:v libx264 -preset veryfast -crf 23 -c:a aac -b:a 128k -hls_time 10 -hls_list_size 0 -f hls {hls_path}"
    run_ffmpeg_command(command)
    
def record_stream(stream_url: str, output_path: str):
    """
    Record a live stream from a URL.

    Args:
        stream_url (str): URL of the live stream to be recorded.
        output_path (str): Path where the recorded stream will be saved.

    This function records a live stream from a given URL and saves it to a file.
    - `-c copy`: Copies the audio and video streams without re-encoding.
    """
    command = f"ffmpeg -i {stream_url} -c copy {output_path}"
    run_ffmpeg_command(command)
