from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import shutil
import os
import uuid
from ..utils import ffmpeg_commands

ffmpeg_router = APIRouter(
    tags=["ffmpeg"], prefix="/ffmpeg", responses={404: {"description": "Not found"}}
)

TEMP_DIR = "storage/temp"
os.makedirs(TEMP_DIR, exist_ok=True)


@ffmpeg_router.post("/merge_audio-video")
async def merge_audio_video(
    audio_file: UploadFile = File(...), video_file: UploadFile = File(...)
):
    # Generate unique temp file paths inside storage/temp
    temp_audio_path = os.path.join(
        TEMP_DIR, f"audio_{uuid.uuid4()}_{audio_file.filename}"
    )
    temp_video_path = os.path.join(
        TEMP_DIR, f"video_{uuid.uuid4()}_{video_file.filename}"
    )
    output_file = os.path.join(TEMP_DIR, f"merged_{uuid.uuid4()}.mp4")

    try:
        # Save uploaded files
        with open(temp_audio_path, "wb") as f:
            shutil.copyfileobj(audio_file.file, f)
        with open(temp_video_path, "wb") as f:
            shutil.copyfileobj(video_file.file, f)

        # Call your ffmpeg merge function
        await ffmpeg_commands.merge_audio_video(
            temp_audio_path, temp_video_path, output_file
        )

        if not os.path.exists(output_file):
            raise HTTPException(status_code=500, detail="Failed to create merged video")

        # Return the merged file as a streaming response
        return FileResponse(
            output_file, media_type="video/mp4", filename="merged_video.mp4"
        )

    finally:
        # Clean up temp input files (keep output if you want)
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)
