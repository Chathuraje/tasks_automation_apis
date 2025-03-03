from app.automations.crypto_cyber_news.models.news_model import VideoResponse
from app.core.gdown import download_file_from_drive
import os
import logging

async def generate(video_data):
    try:
        folder_url = "https://drive.google.com/uc?export=download&id="
        
        os.makedirs("./tmp", exist_ok=True)
        directory = "./tmp/" + video_data.notion_id
        os.mkdir(directory)

        audio_path = os.path.join(directory, "audio.mp3")
        await download_file_from_drive(folder_url + video_data.audio_id, audio_path)
        logging.info(f"Downloaded audio to {audio_path}")

        image_path = os.path.join(directory, "image.png")
        await download_file_from_drive(folder_url + video_data.image_id, image_path)
        logging.info(f"Downloaded image to {image_path}")

        data_path = os.path.join(directory, "data.json")
        await download_file_from_drive(folder_url + video_data.data_id, data_path)
        logging.info(f"Downloaded data to {data_path}")

        # generate the video
        video_id = "some_generated_video_id"  # Replace with actual video generation logic
        logging.info(f"Video generated with ID: {video_id}")

        return {"video_id": video_id, "notion_id": video_data.notion_id}
    except Exception as e:
        logging.error(f"Error generating video: {str(e)}")
        return {"error": str(e)}
