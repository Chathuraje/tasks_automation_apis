from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
import os
import uuid
import asyncio
import sys
from ..utils import ffmpeg_commands, video_generation

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

video_generation_routes = APIRouter(
    prefix="/video_generation", responses={404: {"description": "Not found"}}
)

TEMP_DIR = "storage/temp"
os.makedirs(TEMP_DIR, exist_ok=True)


@video_generation_routes.post("/upload-audio-video")
async def upload_audio_video(
    file_type: str,  # expects 'audio' or 'video'
    file: UploadFile = File(...),
):
    # Sanitize and validate file_type
    file_type = file_type.lower()
    if file_type not in ["audio", "video"]:
        return {"error": "Invalid file_type. Must be 'audio' or 'video'."}

    # Create a new filename using UUID and file_type
    new_filename = f"{file_type}_{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(TEMP_DIR, new_filename)

    # Save the uploaded file
    await video_generation.save_upload_file(file, file_path)

    return {
        "file_type": file_type,
        "saved_filename": new_filename,
    }


@video_generation_routes.post("/merge_audio-video")
async def merge_audio_video(
    background_tasks: BackgroundTasks, audio_file: str, video_file: str
):
    # Save uploaded input files with unique names
    temp_audio_path = os.path.join(TEMP_DIR, audio_file)
    temp_video_path = os.path.join(TEMP_DIR, video_file)

    # Output temporary filename (.tmp)
    output_tmp_filename = f"merged_{uuid.uuid4()}.mp4"
    output_tmp_path = os.path.join(TEMP_DIR, output_tmp_filename)

    # Check if input files exist
    if not os.path.isfile(temp_audio_path):
        raise HTTPException(
            status_code=400,
            detail={"success": False, "message": "Audio file not found."},
        )
    if not os.path.isfile(temp_video_path):
        raise HTTPException(
            status_code=400,
            detail={"success": False, "message": "Video file not found."},
        )

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


# check if generation compelted
@video_generation_routes.get("/check_generation/{filename}")
async def check_generation(filename: str):
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
        return {
            "success": False,
            "message": "Generation in progress or file not found",
        }

    return {
        "success": True,
        "message": "Generation completed",
        "filename": filename,
    }


@video_generation_routes.get("/files/{filename}")
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
