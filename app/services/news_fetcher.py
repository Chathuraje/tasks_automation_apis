import requests
from datetime import datetime, timedelta
from fastapi import HTTPException
from app.core.config import config

def fetch_crypto_news():
    """
    Fetch latest financial & cryptocurrency news using NewsAPI.

    - Uses predefined keywords to find relevant news.
    - Filters news from the past two days.
    - Sorts articles by the most recent publish date.
    - Returns a structured list of news articles.
    """

    if not config.NEWS_API_KEY:
        raise HTTPException(status_code=500, detail="News API key is missing. Set NEWS_API_KEY in .env")

    # Get today's date and two days back date in 'YYYY-MM-DD' format
    today = datetime.utcnow().date()
    from_date = (today - timedelta(days=2)).strftime("%Y-%m-%d")

    # Define relevant keywords for finance & crypto impact
    keywords = "crypto OR bitcoin OR ethereum OR crypto market"

    # API request parameters
    params = {
        "q": keywords,  # Search for critical finance & crypto news
        "from": from_date,  # Fetching news from two days ago
        "to": today.strftime("%Y-%m-%d"),  # Up to today
        "sortBy": "publishedAt",  # Sorting by most recent articles
        "language": "en",  # Fetch only English news
        "pageSize": 10,  # Limit to 10 articles
        "apiKey": config.NEWS_API_KEY
    }

    # Make a request to NewsAPI
    response = requests.get(config.NEWS_API_BASE_URL, params=params)
    
    # Check if API request was successful
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch news")

    data = response.json()

    # Validate API response
    if "articles" not in data:
        raise HTTPException(status_code=500, detail="Invalid response from NewsAPI")

    # Extract relevant fields from the articles
    return [
        {
            "author": article.get("author"),
            "title": article.get("title"),
            "description": article.get("description"),
            "publishedAt": article.get("publishedAt"),
            "url": article.get("url"),
        }
        for article in data["articles"]
    ]
