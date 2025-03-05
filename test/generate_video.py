import json
import os
from app.automations.ccn.models.news_model import VideoResponse
from app.features.gdown import download_file_from_drive
from fastapi import HTTPException
from moviepy import *


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

        image_path = os.path.join(directory, "image.png")
        await download_file_from_drive(folder_url + video_data.image_id, image_path)

        data_path = os.path.join(directory, "transcription.json")
        await download_file_from_drive(
            folder_url + video_data.transcription_id, data_path
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

    try:
        # Paths
        image_path = os.path.join(directory, "image.png")
        audio_path = os.path.join(directory, "audio.mp3")
        transcription_path = os.path.join(directory, "transcription.json")

        # Read JSON data
        with open(transcription_path, "r", encoding="utf-8") as f:
            transcription_data = json.load(f)

        # Generate the video
        output_video_path = os.path.join(directory, "output.mp4")

        # Load the audio file
        audio = AudioFileClip(audio_path)

        image_clip = ImageClip(
            image_path, duration=audio.duration
        )  # Create an ImageClip, setting the duration to match the audio
        image_clip = image_clip.resized(
            width=1080, height=1920
        )  # Set the image size explicitly (optional, but prevents some issues)
        video_clip = image_clip.with_audio(audio)  # Set the audio to the video

        # Initialize an empty list to hold subtitle clips
        subtitle_clips = []

        # Loop through the transcription data and generate subtitle clips
        for data_item in transcription_data:
            for sentence in data_item["sentences"]:
                for word in sentence["words"]:
                    
                    sentence_data = {
                        "word": word["text"],
                        "start": word["start"],
                        "end": word["end"],
                    }
                    subtitle_clips.append(sentence_data)
                
                    # start_time = sentence["start"]
                    # end_time = sentence["end"]

                    # # Create a TextClip for each sentence
                    # text_clip = TextClip(
                    #     font="Arial.ttf",
                    #     text=sentence["text"],
                    #     font_size=70,
                    #     color="white",
                    #     stroke_width=2,
                    #     stroke_color="black",
                    #     method="caption",
                    #     text_align="center",
                    #     size=(1080, None)
                    # )

                    # # Set the duration and timing for the subtitle
                    
                    # text_clip = text_clip.with_duration(end_time - start_time)
                    
                    
        print(subtitle_clips)

                # Add the subtitle clip to the list
                

        # Combine the video and subtitle clips
        # final_video = CompositeVideoClip([video_clip] + subtitle_clips)
        # final_video.preview()
        
        # Create a preview video by limiting the duration to the first 10 seconds
        # preview_duration = 10  # 10 seconds preview
        # preview_video = final_video.subclipped(0, preview_duration)
        # preview_video.write_videofile(
        #     output_video_path, fps=25, codec="libx264", audio_codec="aac"
        # )

        # Set the final video format and frame rate
        # final_video.write_videofile(
        #     output_video_path, fps=25, codec="libx264", audio_codec="aac"
        # )

        # Return video ID
        video_id = f"video_{video_data.notion_id}"
        return {"video_id": video_id, "notion_id": video_data.notion_id}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to generate video: {str(e)}"
        )
