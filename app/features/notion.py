import requests
from fastapi import HTTPException
from app.features.config import config

NOTION_API_URL = "https://api.notion.com/v1/databases/{database_id}/query"
NOTION_HEADERS = {
    "Authorization": f"Bearer {config.GLOBAL_NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def query_notion_database(DB_ID):
    """
    Fetch all entries from the specified Notion database.
    Returns the JSON response or raises an error if the request fails.
    """

    url = NOTION_API_URL.format(database_id=DB_ID)

    response = requests.post(url, headers=NOTION_HEADERS, json={})

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch Notion database entries")

    return response.json()
