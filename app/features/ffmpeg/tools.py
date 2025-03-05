from pydub.utils import mediainfo

def get_audio_duration(audio_path: str) -> str:
    """Get the duration of an audio file using pydub."""
    audio_info = mediainfo(audio_path)
    duration = audio_info['duration']
    
    # Round and add 2 seconds
    duration_seconds = round(float(duration)) + 1
    
    return duration_seconds
