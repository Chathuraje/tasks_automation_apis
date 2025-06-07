from fastapi import UploadFile, HTTPException, Request
from app.core.tools import google_drive, youtube
import asyncio
import uuid
from typing import Dict
import os
import json
from app.core.tools.youtube import authorize, oauth2callback


UPLOAD_STATUS_FILE = "app/api/v1/tuneezy/video_generation/storage/video_upload.json"
YOUTUBE_UPLOAD_STATUS_FILE = "app/api/v1/tuneezy/video_generation/storage/youtube_upload.json"

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
REDIRECT_URI = "http://localhost:8000/api/v1/tuneezy/video_generation/oauth2callback"


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
    file_id = await google_drive.upload_file(
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
    if upload_id in google_drive.upload_progress:
        return {
            "video_id": "0",
            "percent_complete": google_drive.upload_progress[upload_id],
            "status": "in_progress",
            "uploaded_at": None,
        }

    # If not found in either
    raise HTTPException(status_code=404, detail="Upload ID not found")


async def youtube_auth(CLIENT_SECRETS: str):
    return authorize(
        application="tuneezy",
        CLIENT_SECRETS=CLIENT_SECRETS,
        SCOPES=SCOPES,
        REDIRECT_URI=REDIRECT_URI,
    )


async def youtube_auth_callback(request: Request):
    """
    Handles the OAuth2 callback from YouTube.
    """
    return await oauth2callback(
        application="tuneezy",
        request=request,
    )


def run_upload_youtube_video(
    file_path: str,
    title: str,
    description: str,
    tags: str,
    category_id: str,
    privacy_status: str,
    upload_id: str
):
    return asyncio.run(
        upload_youtube_video(
            file_path,
            title,
            description,
            tags,
            category_id,
            privacy_status,
            upload_id
        )
    )

async def upload_youtube_video(
    file_path: str,
    title: str,
    description: str,
    tags: str,
    category_id: str,
    privacy_status: str,
    upload_id: str
):
    
    file_id = await youtube.upload_file(
        application="tuneezy",
        file_path=file_path,
        title=title,
        description=description,
        tags=tags,
        category_id=category_id,
        privacy_status=privacy_status,
        upload_id=upload_id
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
    if os.path.exists(YOUTUBE_UPLOAD_STATUS_FILE):
        with open(YOUTUBE_UPLOAD_STATUS_FILE, "r") as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = {}
    else:
        existing_data = {}

    # Update and save
    existing_data.update(result_data)
    with open(YOUTUBE_UPLOAD_STATUS_FILE, "w") as f:
        json.dump(existing_data, f, indent=4)
        
        
async def get_youtube_upload_progress(upload_id: str):
    """
    Get the upload progress for a specific upload ID.

    Args:
        upload_id (str): The unique ID for the upload.

    Returns:
        int: The current upload progress percentage.
    """

    # First check the JSON file for completed uploads
    if os.path.exists(YOUTUBE_UPLOAD_STATUS_FILE):
        with open(YOUTUBE_UPLOAD_STATUS_FILE, "r") as f:
            try:
                data = json.load(f)
                if upload_id in data:
                    return data[upload_id]
            except json.JSONDecodeError:
                pass  # Ignore corrupted file and fall back to in-memory progress

    # If not found in file, check the in-memory progress
    if upload_id in youtube.upload_progress:
        return {
            "video_id": "0",
            "percent_complete": youtube.upload_progress[upload_id],
            "status": "in_progress",
            "uploaded_at": None,
        }

    # If not found in either
    raise HTTPException(status_code=404, detail="Upload ID not found")