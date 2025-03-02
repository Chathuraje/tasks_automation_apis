import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Global variables
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    NOTION_API_KEY = os.getenv("NOTION_API_KEY")
    
    # Crypto Cyber News
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    NEWS_API_BASE_URL = "https://newsapi.org/v2/everything"
    DAILY_ARTICLE_DB_NOTION = os.getenv("DAILY_ARTICLE_DB_NOTION")

config = Config()
