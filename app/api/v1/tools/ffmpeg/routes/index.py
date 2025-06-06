from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
import shutil
import os
import uuid
import asyncio
import sys
from ..utils import ffmpeg_commands

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

ffmpeg_router = APIRouter(
    tags=["ffmpeg"], prefix="/ffmpeg", responses={404: {"description": "Not found"}}
)

TEMP_DIR = "storage/temp"
os.makedirs(TEMP_DIR, exist_ok=True)


@ffmpeg_router.post("/merge_audio-video")
async def merge_audio_video(
    background_tasks: BackgroundTasks,
    audio_file: UploadFile = File(...),
    video_file: UploadFile = File(...),
):
    # Save uploaded input files with unique names
    temp_audio_path = os.path.join(
        TEMP_DIR, f"audio_{uuid.uuid4()}_{audio_file.filename}"
    )
    temp_video_path = os.path.join(
        TEMP_DIR, f"video_{uuid.uuid4()}_{video_file.filename}"
    )

    # Output temporary filename (.tmp)
    output_tmp_filename = f"merged_{uuid.uuid4()}.mp4"
    output_tmp_path = os.path.join(TEMP_DIR, output_tmp_filename)

    # Save uploaded files to disk
    await ffmpeg_commands.save_upload_file(audio_file, temp_audio_path)
    await ffmpeg_commands.save_upload_file(video_file, temp_video_path)

    # Schedule background merge task
    background_tasks.add_task(
        ffmpeg_commands.run_merge_audio_video,
        temp_audio_path,
        temp_video_path,
        output_tmp_path,
    )

    # replace merged_ with empty string to get final filename
    output_final_filename = output_tmp_filename.replace("merged_", "")

    # Immediately return the final filename (client can poll /files/{filename})
    return {"filename": output_final_filename}


@ffmpeg_router.get("/files/{filename}")
async def get_file(filename: str):
    # Prevent directory traversal attack
    if ".." in filename or filename.startswith("/"):
        raise HTTPException(
            status_code=200,
            detail={
                "success": False,
                "message": "Invalid filename",
            },
        )

    if filename.endswith(".tmp"):
        raise HTTPException(
            status_code=200,
            detail={
                "success": False,
                "message": "Temporary files cannot be accessed directly",
            },
        )

    file_path = os.path.join(TEMP_DIR, filename)

    if not os.path.isfile(file_path):
        raise HTTPException(
            status_code=200,
            detail={
                "success": False,
                "message": "Generation in progress or file not found",
            },
        )

    return FileResponse(file_path, filename=filename)
