import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    # Global variables
    GLOBAL_OPENAI_API_KEY = os.getenv("GLOBAL_OPENAI_API_KEY")
    GLOBAL_NOTION_API_KEY = os.getenv("GLOBAL_NOTION_API_KEY")
    GLOBAL_GOOGLE_CLIENT_ID = os.getenv("GLOBAL_GOOGLE_CLIENT_ID")
    GLOBAL_GOOGLE_CLIENT_SECRET = os.getenv("GLOBAL_GOOGLE_CLIENT_SECRET")

    # Crypto Cyber News
    CCN_NEWS_API_KEY = os.getenv("CCN_NEWS_API_KEY")
    CCN_DAILY_ARTICLE_DB_NOTION = os.getenv("CCN_DAILY_ARTICLE_DB_NOTION")


config = Config()
