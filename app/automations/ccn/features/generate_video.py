import json
import os
from app.automations.ccn.models.news_model import VideoResponse
from app.features.gdown import download_file_from_drive
from fastapi import HTTPException
from moviepy import *

from app.features.ffmpeg.video import merge_audio_video
from app.features.ffmpeg.tools import get_audio_duration
from app.features.ffmpeg.subtitle import add_permanent_subtitles, convert_srt_to_ass
import random

# Download assets from Google Drive
async def download_content(video_data):
    try:
        folder_url = "https://drive.google.com/uc?export=download&id="

        os.makedirs("./storage", exist_ok=True)
        os.makedirs("./storage/ccn", exist_ok=True)
        directory = f"./storage/ccn/{video_data.notion_id}"
        os.makedirs(directory, exist_ok=True)

        # Download audio, image, and JSON data
        audio_path = os.path.join(directory, "audio.mp3")
        await download_file_from_drive(folder_url + video_data.audio_id, audio_path)
        
        directory_videos = "./app/automations/ccn/resources/videos.json"
        video_path = os.path.join(directory, "video.mp4")
        # Find a id from the videos.json
        with open(directory_videos, 'r') as file:
            data = json.load(file)
            # Shuffle the list of ids and pick a random one
            random_id = random.choice(data["ids"])
            await download_file_from_drive(folder_url + random_id, video_path)

        transcription_path = os.path.join(directory, "transcription.srt")
        await download_file_from_drive(
            folder_url + video_data.transcription_id, transcription_path
        )

        return directory

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to download content: {str(e)}"
        )


# Generate the video with subtitles
async def generate(video_data):
    # YouTube Shorts dimensions
    shorts_size = (1080, 1920)

    directory = await download_content(video_data)
    if not directory:
        raise HTTPException(status_code=400, detail="Failed to download content")

    # Paths
    video_path = directory + "/video.mp4"
    audio_path = directory + "/audio.mp3"
    transcription_path = directory + "/transcription.srt"
    tmp_video_path = directory + "/output.mp4"
    final_video_path = directory + "/" + video_data.notion_id + ".mp4"
    
    if not os.path.exists(tmp_video_path):
        merge_audio_video(video_path, audio_path, tmp_video_path, loop=True)
        
    if not os.path.exists(final_video_path):
        # ass_path = directory + "/transcription.ass"
        # convert_srt_to_ass(transcription_path, ass_path)
        
        style = "Fontname=Roboto,Fontsize=22,OutlineColour=&H40000000,Bold=1,BackColour=&H00000000,Spacing=0.2,Outline=0,Shadow=0.75,Alignment=2"
        add_permanent_subtitles(tmp_video_path, transcription_path, final_video_path, style)

    # Return video ID
    video_id = f"video_{video_data.notion_id}"
    return {"video_id": video_id, "notion_id": video_data.notion_id}