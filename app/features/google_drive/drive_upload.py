from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from fastapi import UploadFile, HTTPException
from .auth import get_credentials
import io
import os

async def upload_to_drive(file_path: str, folder_id: str, account_id: str):
    """Uploads a video file to a specific Google Drive folder."""
    creds = get_credentials(account_id)
    service = build("drive", "v3", credentials=creds)

    file_metadata = {
        "name": os.path.basename(file_path),
        "mimeType": "video/mp4",
        "parents": [folder_id],  # Set the target folder ID
    }
    
    with open(file_path, "rb") as f:
        media = MediaIoBaseUpload(io.BytesIO(f.read()), mimetype="video/mp4", resumable=True)

    try:
        file_drive = service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id, name, parents"
        ).execute()
        return {
            "file_id": file_drive.get("id"),
            "file_name": file_drive.get("name"),
            "folder_id": file_drive.get("parents"),
            "message": "Upload successful!"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


