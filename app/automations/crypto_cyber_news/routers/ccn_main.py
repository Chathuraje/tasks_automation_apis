from fastapi import APIRouter, HTTPException
from app.automations.crypto_cyber_news.features.news_fetcher import fetch_crypto_news
from app.automations.crypto_cyber_news.models.news_model import NewsResponse
from app.automations.crypto_cyber_news.features.ask_gpt import process_news_articles

# Initialize router for news-related endpoints
router = APIRouter(prefix="/crypto_cyber_news", tags=["Crypto Cyber News"])

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
        "seo_tags": processed_result["seo_tags"],
        "image_prompts": processed_result["image_prompts"]
    }

