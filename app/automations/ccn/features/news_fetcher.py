import requests
from datetime import datetime, timedelta
from fastapi import HTTPException
from app.features.config import config
from app.automations.ccn.features.notion import get_uploaded_titles_from_notion

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
    keywords = "crypto OR bitcoin OR ethereum"

    # API request parameters
    params = {
        "q": keywords,  # Search for critical finance & crypto news
        "from": from_date,  # Fetching news from two days ago
        "to": today.strftime("%Y-%m-%d"),  # Up to today
        "sortBy": "publishedAt",  # Sorting by most recent articles
        "language": "en",  # Fetch only English news
        "pageSize": 12,  # Limit to 10 articles
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
    
    # Retrieve the list of already uploaded article titles from Notion
    uploaded_titles = get_uploaded_titles_from_notion()

    # Initialize an empty list to store filtered articles
    filtered_articles = []
    # Iterate through each article in the dataset
    for article in data["articles"]:
        # Extract the title of the article
        article_title = article.get("title")
        
        # Check if the article has a valid title and if it is not already uploaded
        if article_title and article_title not in uploaded_titles:
            # Create a dictionary containing the title and URL of the article
            filtered_article = {
                "title": article_title,
                "url": article.get("url")
            }
            
            # Append the filtered article to the list
            filtered_articles.append(filtered_article)
            
        if len(filtered_articles) >= 5:
            break


    return filtered_articles
