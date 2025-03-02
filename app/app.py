from fastapi import FastAPI, Depends, HTTPException, Header
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Retrieve API keys from .env file
API_KEY = os.getenv("NEWS_API_KEY")
AUTH_API_KEY = os.getenv("AUTH_API_KEY")  # API key for authentication
NEWS_API_BASE_URL = "https://newsapi.org/v2/everything"

def authenticate(api_key: str = Header(None)):
    """Dependency to authenticate API requests using an API key"""
    if not api_key or api_key != AUTH_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return api_key

@app.get("/")
def read_root():
    """Root endpoint to verify the API is running"""
    return {"message": "Hello, Crypto Cyber News!"}

@app.get("/news")
def get_crypto_finance_news(api_key: str = Depends(authenticate)):
    """
    Fetch latest financial & cryptocurrency news that might affect the market.
    
    - Requires a valid API key via `api_key` header.
    - Filters relevant topics such as crypto, Bitcoin, Ethereum, regulation, and market trends.
    - Limits results to 10 most recent articles.
    - Limits sources to major financial & business news providers.
    - Sorts articles by newest first.
    """
    if not API_KEY:
        raise HTTPException(status_code=500, detail="News API key is missing. Set NEWS_API_KEY in .env")

    # Get today's date and two days back date in 'YYYY-MM-DD' format
    today = datetime.utcnow().date()
    from_date = (today - timedelta(days=2)).strftime("%Y-%m-%d")

    # Define relevant keywords for finance & crypto impact
    keywords = "crypto OR bitcoin OR ethereum OR crypto market"

    # API request parameters with finance-relevant sources
    params = {
        "q": keywords,  # Search for critical finance & crypto news
        "from": from_date,  # Fetching news from two days ago
        "to": today.strftime("%Y-%m-%d"),  # Up to today
        "sortBy": "publishedAt",  # Sorting by most recent articles
        "language": "en",  # Fetch only English news
        "pageSize": 10,  # Limit to 10 articles
        "apiKey": API_KEY
    }

    # Make a request to NewsAPI
    response = requests.get(NEWS_API_BASE_URL, params=params)
    
    # Check if API request was successful
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch news")

    data = response.json()

    # Check if the response contains articles
    if "articles" not in data:
        raise HTTPException(status_code=500, detail="Invalid response from NewsAPI")

    # Extract relevant fields from the articles
    articles = [
        {
            "author": article.get("author"),
            "title": article.get("title"),
            "description": article.get("description"),
            "publishedAt": article.get("publishedAt"),
            "url": article.get("url"),
        }
        for article in data["articles"]
    ]

    # Ensure sorting by 'publishedAt' in descending order (newest first)
    articles.sort(key=lambda x: x["publishedAt"], reverse=True)

    return {"status": "ok", "totalResults": len(articles), "articles": articles}
