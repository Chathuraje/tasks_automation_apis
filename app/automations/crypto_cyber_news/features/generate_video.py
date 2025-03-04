import json
import os
from app.automations.crypto_cyber_news.models.news_model import VideoResponse
from app.features.gdown import download_file_from_drive
from fastapi import HTTPException

# Function to generate subtitle timings dynamically
def generate_srt(script_text, words_per_second=3):
    words = script_text.split()
    subtitles = []
    start_time = 0
    chunk_size = 5  # Approx. 5 words per subtitle
    for i in range(0, len(words), chunk_size):
        line = " ".join(words[i : i + chunk_size])
        duration = len(line.split()) / words_per_second
        end_time = start_time + duration
        subtitles.append((start_time, end_time, line))
        start_time = end_time
    return subtitles

# Download assets from Google Drive
async def download_content(video_data):
    try:
        folder_url = "https://drive.google.com/uc?export=download&id="

        os.makedirs("./storage", exist_ok=True)
        os.makedirs("./storage/crypto_cyber_news", exist_ok=True)
        directory = f"./storage/crypto_cyber_news/{video_data.notion_id}"
        os.makedirs(directory, exist_ok=True)

        # Download audio, image, and JSON data
        audio_path = os.path.join(directory, "audio.mp3")
        await download_file_from_drive(folder_url + video_data.audio_id, audio_path)

        image_path = os.path.join(directory, "image.png")
        await download_file_from_drive(folder_url + video_data.image_id, image_path)

        data_path = os.path.join(directory, "data.json")
        await download_file_from_drive(folder_url + video_data.data_id, data_path)

        return directory

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download content: {str(e)}")

# Generate the video with subtitles
async def generate(video_data):
    directory = await download_content(video_data)
    if not directory:
        raise HTTPException(status_code=400, detail="Failed to download content")

    try:
        # Paths
        image_path = os.path.join(directory, "image.png")
        audio_path = os.path.join(directory, "audio.mp3")
        data_path = os.path.join(directory, "data.json")

        # Read JSON data
        with open(data_path, 'r', encoding="utf-8") as f:
            data = json.load(f)
        script_text = data["script"]

        # Generate subtitles
        subtitles = generate_srt(script_text)
        print(subtitles)

        # Return video ID
        video_id = f"video_{video_data.notion_id}"
        return {"video_id": video_id, "notion_id": video_data.notion_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate video: {str(e)}")
