import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
import json
from googleapiclient.http import MediaIoBaseUpload

# Global or external dictionary to store progress
upload_progress = {}

CHUNK_SIZE = 256 * 1024


async def upload_file(file_name, file_path, folder_id, service_account_data, upload_id):
    """
    Uploads a file to a specific Google Drive folder using a service account JSON (dict).

    Args:
        file_path (str): Local path to the video file.
        folder_id (str): ID of the target Google Drive folder.
        service_account_data (dict): Parsed JSON content of the service account.

    Returns:
        str: The file ID of the uploaded file on Google Drive.
    """

    SCOPES = ["https://www.googleapis.com/auth/drive.file"]

    service_account_json = json.loads(service_account_data)

    # Load credentials from dict (not file)
    creds = service_account.Credentials.from_service_account_info(
        service_account_json, scopes=SCOPES
    )

    service = build("drive", "v3", credentials=creds)

    file_metadata = {
        "name": file_name,
        "parents": [folder_id],
    }

    media = MediaFileUpload(file_path, mimetype="video/mp4", resumable=True)

    request = service.files().create(body=file_metadata, media_body=media, fields="id")

    print(f"Starting upload: {file_name}...")
    response = None
    upload_progress[upload_id] = 0

    with open(file_path, "rb") as f:
        media = MediaIoBaseUpload(
            f, mimetype="video/mp4", chunksize=CHUNK_SIZE, resumable=True
        )
        request = service.files().create(
            body=file_metadata, media_body=media, fields="id"
        )

        response = None
        upload_progress[upload_id] = 0

        while response is None:
            status, response = request.next_chunk()
            if status:
                progress = int(status.progress() * 100)
                upload_progress[upload_id] = progress

    print(f"Upload complete! File ID: {response.get('id')}")
    upload_progress[upload_id] = 100  # Ensure final update

    return response.get("id")
