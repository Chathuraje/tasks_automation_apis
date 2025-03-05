from fastapi import HTTPException
from app.features.config import config
from app.features.notion import query_notion_database

def get_uploaded_titles_from_notion():
    """
    Retrieve a list of already uploaded news titles from the Notion database.
    """
    
    
    data = query_notion_database(config.CCN_DAILY_ARTICLE_DB_NOTION)
    
    if "results" not in data:
        raise HTTPException(status_code=500, detail="Invalid response from Notion API")

    return {
        entry["properties"]["Article Title"]["title"][0]["text"]["content"]
        for entry in data["results"]
        if "Article Title" in entry["properties"] and entry["properties"]["Article Title"]["title"]
    }