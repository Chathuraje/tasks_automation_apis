import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    NEWS_API_BASE_URL = "https://newsapi.org/v2/everything"
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

config = Config()
