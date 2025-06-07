from fastapi import Request
from fastapi.responses import JSONResponse
from google_auth_oauthlib.flow import Flow
import os
import json
import pickle
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

auth_flows = {}

# Global or external dictionary to store progress
upload_progress = {}

CHUNK_SIZE = 256 * 1024


def authorize(application: str, CLIENT_SECRETS: str, SCOPES: list, REDIRECT_URI: str):
    """
    Start the OAuth flow and return the authorization URL.
    """
    
    secrets_dir = f"app/api/v1/{application}/video_generation/storage/secrets"
    os.makedirs(secrets_dir, exist_ok=True)

    CLIENT_SECRETS_FILE = os.path.join(secrets_dir, f"{application}_google_secret.json")

    try:
        client_secrets = json.loads(CLIENT_SECRETS)
        with open(CLIENT_SECRETS_FILE, "w") as f:
            json.dump(client_secrets, f, indent=4)
    except json.JSONDecodeError as e:
        return {"status": "error", "message": f"Invalid JSON format: {str(e)}"}

    try:
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, scopes=SCOPES, redirect_uri=REDIRECT_URI
        )
        auth_url, state = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
            prompt="consent", 
        )

        # Store flow temporarily using unique state key
        auth_flows[state] = flow

        return {
            "status": "success",
            "message": "Authorization URL generated successfully.",
            "auth_url": auth_url,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def oauth2callback(application: str, request: Request):
    """
    Callback after user authorizes app. Saves credentials.
    """
    CREDENTIALS_DIR = f"app/api/v1/{application}/video_generation/storage/credentials"
    os.makedirs(CREDENTIALS_DIR, exist_ok=True)
    CREDENTIALS_PICKLE_FILE = os.path.join(
        CREDENTIALS_DIR, f"{application}_google_credentials.pickle"
    )

    state = request.query_params.get("state")
    code = request.query_params.get("code")

    if not state or state not in auth_flows:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": "Invalid state or session expired."},
        )

    flow = auth_flows.pop(state)  # Remove flow from memory once used
    try:
        flow.fetch_token(code=code)
        creds = flow.credentials

        with open(CREDENTIALS_PICKLE_FILE, "wb") as token:
            pickle.dump(creds, token)

        return JSONResponse(
            status_code=200,
            content={"status": "success", "message": "Authorization complete."},
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Failed to fetch token: {str(e)}"},
        )


async def upload_file(
    application: str,
    file_path: str,
    title: str,
    description: str,
    tags: str,
    category_id: str,
    privacy_status: str,
    upload_id: str
):
    """
    Uploads a video to YouTube using the YouTube Data API.

    Args:
        filename (str): The path to the video file to upload.
        title (str): The title of the video.
        description (str): The description of the video.
        tags (str): Comma-separated tags for the video.
        category_id (str): The category ID for the video.
        privacy_status (str): The privacy status of the video ("public", "private", "unlisted").

    Returns:
        dict: A dictionary containing the upload status and video ID.
    """
    CREDENTIALS_DIR = f"app/api/v1/{application}/video_generation/storage/credentials"
    CREDENTIALS_PICKLE_FILE = os.path.join(
        CREDENTIALS_DIR, f"{application}_google_credentials.pickle"
    )

    if not os.path.exists(CREDENTIALS_PICKLE_FILE):
        return {
            "status": "error",
            "message": "YouTube API credentials not found. Please authenticate first."
        }

    try:
        with open(CREDENTIALS_PICKLE_FILE, "rb") as token:
            creds = pickle.load(token)

        youtube = build("youtube", "v3", credentials=creds)

        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": [tag.strip() for tag in tags.split(",") if tag.strip()],
                "categoryId": category_id,
            },
            "status": {
                "privacyStatus": privacy_status,
            }
        }

        media = MediaFileUpload(file_path, chunksize=CHUNK_SIZE, resumable=True)

        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
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

    except HttpError as e:
        return {
            "status": "error",
            "message": f"YouTube API error: {e.resp.status} - {e._get_reason()}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Unexpected error: {str(e)}"
        }