from fastapi import UploadFile, HTTPException
from app.core.tools.google_drive import upload_file
import asyncio
import uuid
from typing import Dict
from app.core.tools.google_drive import upload_progress
import os
import json

UPLOAD_STATUS_FILE = "app/api/v1/tuneezy/video_generation/storage/video_upload.json"


# Utility to save uploaded file
async def save_upload_file(upload_file: UploadFile, destination: str):
    with open(destination, "wb") as out_file:
        content = await upload_file.read()
        out_file.write(content)


def run_upload_file_to_google_drive(
    file_name: str,
    file_path: str,
    folder_id: str,
    service_account_data: str,
    upload_id: str,
):
    asyncio.run(
        upload_file_to_google_drive(
            file_name, file_path, folder_id, service_account_data, upload_id
        )
    )


# Utility to upload file to the google drive
async def upload_file_to_google_drive(
    file_name: str,
    file_path: str,
    folder_id: str,
    service_account_data: str,
    upload_id: str,
):

    # Upload the file to Google Drive
    file_id = await upload_file(
        file_name, file_path, folder_id, service_account_data, upload_id
    )

    # Prepare the result data
    result_data = {
        upload_id: {
            "video_id": file_id,
            "percent_complete": 100,
            "status": "completed",
            "uploaded_at": str(os.path.getmtime(file_path)),
        }
    }

    # Load existing JSON data if file exists
    if os.path.exists(UPLOAD_STATUS_FILE):
        with open(UPLOAD_STATUS_FILE, "r") as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = {}
    else:
        existing_data = {}

    # Update and save
    existing_data.update(result_data)
    with open(UPLOAD_STATUS_FILE, "w") as f:
        json.dump(existing_data, f, indent=4)


async def get_upload_progress(upload_id: str):
    """
    Get the upload progress for a specific upload ID.

    Args:
        upload_id (str): The unique ID for the upload.

    Returns:
        int: The current upload progress percentage.
    """

    # First check the JSON file for completed uploads
    if os.path.exists(UPLOAD_STATUS_FILE):
        with open(UPLOAD_STATUS_FILE, "r") as f:
            try:
                data = json.load(f)
                if upload_id in data:
                    return data[upload_id]
            except json.JSONDecodeError:
                pass  # Ignore corrupted file and fall back to in-memory progress

    # If not found in file, check the in-memory progress
    if upload_id in upload_progress:
        return {
            "video_id": "0",
            "percent_complete": upload_progress[upload_id],
            "status": "in_progress",
            "uploaded_at": None,
        }

    # If not found in either
    raise HTTPException(status_code=404, detail="Upload ID not found")
