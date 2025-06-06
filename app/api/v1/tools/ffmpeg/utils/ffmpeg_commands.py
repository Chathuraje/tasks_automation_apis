import os
import shutil
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from app.core.tools.ffmpeg import run_ffmpeg_command

ffmpeg_router = APIRouter()

TEMP_DIR = "storage/temp"
os.makedirs(TEMP_DIR, exist_ok=True)


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


@ffmpeg_router.post("/merge_audio-video")
async def merge_audio_video_endpoint(
    audio_file: UploadFile = File(...), video_file: UploadFile = File(...)
):
    # Save uploaded files to temp folder
    audio_path = os.path.join(TEMP_DIR, f"audio_{uuid.uuid4()}_{audio_file.filename}")
    video_path = os.path.join(TEMP_DIR, f"video_{uuid.uuid4()}_{video_file.filename}")
    output_path = os.path.join(TEMP_DIR, f"merged_{uuid.uuid4()}.mp4")

    try:
        with open(audio_path, "wb") as f:
            shutil.copyfileobj(audio_file.file, f)
        with open(video_path, "wb") as f:
            shutil.copyfileobj(video_file.file, f)

        await merge_audio_video(audio_path, video_path, output_path)

        if not os.path.exists(output_path):
            raise HTTPException(
                status_code=500, detail="Failed to generate merged video"
            )

        # Return the merged file as a streaming response
        return FileResponse(
            output_path, media_type="video/mp4", filename="merged_video.mp4"
        )

    finally:
        # Clean up uploaded files
        for path in [audio_path, video_path]:
            if os.path.exists(path):
                os.remove(path)
