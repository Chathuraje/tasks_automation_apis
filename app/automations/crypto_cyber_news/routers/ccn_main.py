from fastapi import APIRouter, HTTPException
from app.automations.crypto_cyber_news.features.news_fetcher import fetch_crypto_news
from app.automations.crypto_cyber_news.models.news_model import NewsResponse, NewsScrapeResponse, NewsScrape, VideoData
from app.automations.crypto_cyber_news.features.ask_gpt import select_best_news, generate_script_and_seo

# Initialize router for news-related endpoints
router = APIRouter(prefix="/crypto_cyber_news", tags=["Crypto Cyber News"])


@router.get("/scrape-news", response_model=NewsScrapeResponse)
async def scrape_news():
    news = fetch_crypto_news()
    
    if "error" in news:
        raise HTTPException(status_code=400, detail=news["error"])
    
    return {
        "count": len(news),
        "articles": news
    }

@router.post("/find_best_article", response_model=NewsScrape)
async def generate_news_script(articles: list[NewsScrape]):
    
    processed_result = await select_best_news(articles)
    
    if "error" in processed_result:
        raise HTTPException(status_code=400, detail=processed_result["error"])

    return {
        "title": processed_result["title"],
        "url": processed_result["url"],
    }
    
    
@router.post("/generate_script", response_model=NewsResponse)
async def generate_news_script(articles: NewsScrape):
    
    processed_result = await generate_script_and_seo(articles)
    
    if "error" in processed_result:
        raise HTTPException(status_code=400, detail=processed_result["error"])

    return {
        "title": articles.title,
        "url": articles.url,
        "script": processed_result["script"],
        "seo_title": processed_result["seo_title"],
        "seo_description": processed_result["seo_description"],
        "seo_tags": processed_result["seo_tags"],
        "image_prompt": processed_result["image_prompt"]
    }


@router.post("/generate_video")
async def generate_video(video_data: VideoData):
    # TODO: Implement video generation logic based on the provided data
    pass


    # Final Call: https://hook.eu2.make.com/xn3asqws1nj2lflg5vlophebsaxbraf1?file_id=1EaddgYMsot8MRxmGBnPZg84gEutXLjWR&news_id=1abab1fa0ce98151851de27870f967e8