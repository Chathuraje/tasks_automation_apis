from googleapiclient.discovery import build
from .auth import get_credentials
from fastapi import HTTPException

async def file_exists(account_id: str, file_name: str, folder_id: str):
    try:
        """Checks if a file with the same name already exists in the specified folder."""
    
        creds = get_credentials(account_id)
        service = build("drive", "v3", credentials=creds)
        
        query = f"name = '{file_name}' and '{folder_id}' in parents and trashed = false"
        response = service.files().list(q=query, fields="files(id, name)").execute()
        files = response.get("files", [])
        
        if files:
            return files[0]["id"]
        
        return None
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking file existence: {str(e)}")
