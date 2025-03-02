from fastapi import APIRouter
from app.services.news_fetcher import fetch_crypto_news
from app.models.news import NewsResponse

# Initialize router for news-related endpoints
router = APIRouter(prefix="/news", tags=["News"])

@router.get("/", response_model=NewsResponse)
async def get_crypto_finance_news():
    """
    Fetch latest financial & cryptocurrency news using NewsAPI.

    - Uses predefined keywords to find relevant news.
    - Filters news from the past two days.
    - Sorts articles by the most recent publish date.
    - Returns articles in structured JSON format.
    """
    articles = fetch_crypto_news()
    return {"articles": articles}
