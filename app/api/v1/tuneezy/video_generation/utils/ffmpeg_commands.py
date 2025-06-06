import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.tools.ffmpeg import run_ffmpeg_command
import asyncio

ffmpeg_router = APIRouter()

TEMP_DIR = "storage/temp"
os.makedirs(TEMP_DIR, exist_ok=True)


async def save_upload_file(upload_file: UploadFile, destination_path: str):
    with open(destination_path, "wb") as f:
        shutil.copyfileobj(upload_file.file, f)
    upload_file.file.close()


def run_merge_audio_video(audio_path: str, video_path: str, output_tmp_path: str):

    # Run your async merge function and wait for it
    asyncio.run(merge_audio_video(audio_path, video_path, output_tmp_path))

    # Rename merged file to remove "merged_" prefix
    output_final_path = output_tmp_path.replace("merged_", "")
    os.rename(output_tmp_path, output_final_path)

    # Clean up input files after merge
    if os.path.exists(audio_path):
        os.remove(audio_path)
    if os.path.exists(video_path):
        os.remove(video_path)


async def merge_audio_video(audio_file: str, video_file: str, output_file: str) -> str:
    command = [
        "ffmpeg",
        "-y",
        "-stream_loop",
        "-1",  # Loop video infinitely
        "-i",
        video_file,
        "-i",
        audio_file,
        "-shortest",  # Stop when the shortest input ends (the audio)
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        output_file,
    ]
    return await run_ffmpeg_command(command)
