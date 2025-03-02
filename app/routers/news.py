from fastapi import APIRouter, HTTPException
from app.services.news_fetcher import fetch_crypto_news
from app.models.news import NewsResponse
from app.services.ask_gpt import process_news_articles

# Initialize router for news-related endpoints
router = APIRouter(prefix="/news", tags=["News"])

@router.get("/", response_model=NewsResponse)
async def generate_news_script():
    news = fetch_crypto_news()
    
    processed_result = await process_news_articles(news)
    
    if "error" in processed_result:
        raise HTTPException(status_code=400, detail=processed_result["error"])

    print(processed_result)
    return {
        "article_title": processed_result["article_title"],
        "article_url": processed_result["article_url"],
        "script": processed_result["script"],
        "seo_title": processed_result["seo_title"],
        "seo_description": processed_result["seo_description"],
        "seo_tags": processed_result["seo_tags"]
    }

