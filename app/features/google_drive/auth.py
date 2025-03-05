import os
import json
import tempfile
from fastapi import HTTPException
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from app.features.config import config

SCOPES = ["https://www.googleapis.com/auth/drive.file"]

# Create credentials config dynamically
CREDENTIALS_CONFIG = {
    "web": {
        "client_id": config.GLOBAL_GOOGLE_CLIENT_ID,
        "project_id": "global-452819",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": config.GLOBAL_GOOGLE_CLIENT_SECRET,
        "redirect_uris": ["http://127.0.0.1:8000/", "http://localhost:8001/"],
    }
}

def get_credentials(account_id: str):
    Token_Path = "./app/features/google_drive/tokens"
    os.makedirs(Token_Path, exist_ok=True)
    
    creds = None
    TOKEN_FILE = f"{Token_Path}/token_{account_id}.json"

    # Load existing token if available
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # Refresh or get new credentials if needed
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Write the credentials config to a temporary file in text mode
            with tempfile.NamedTemporaryFile("w", delete=False) as tmp_file:
                json.dump(CREDENTIALS_CONFIG, tmp_file)
                tmp_file_path = tmp_file.name

                print(f"Temporary file path: {tmp_file_path}")

            # Load credentials from the temporary file
            flow = InstalledAppFlow.from_client_secrets_file(tmp_file_path, SCOPES, redirect_uri="http://localhost/")
            creds = flow.run_local_server(port=8001)

            # Clean up the temporary file
            os.remove(tmp_file_path)

        # Save new credentials for the specific account
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return creds

