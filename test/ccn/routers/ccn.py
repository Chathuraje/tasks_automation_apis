from fastapi import APIRouter, HTTPException
from app.automations.ccn.features.news_fetcher import fetch_crypto_news
from app.automations.ccn.models.news_model import NewsResponse, NewsScrape, VideoData, VideoResponse
from app.automations.ccn.features.ask_gpt import select_best_news, generate_script_and_seo
from app.automations.ccn.features.generate_video import generate
import httpx

# Initialize router for news-related endpoints
router = APIRouter(prefix="/ccn", tags=["Crypto Cyber News"])


@router.get("/scrape-news", response_model=list[NewsScrape])
async def scrape_news():
    news = fetch_crypto_news()
    
    if "error" in news:
        raise HTTPException(status_code=400, detail=news["error"])
    
    return news

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
    video_response = await generate(video_data)

    if video_response is None:
        raise HTTPException(status_code=400, detail="Error generating video")

    url = f"https://hook.eu2.make.com/47kt0jpyb6mfg3icmccczwq9ht2s3xry?video_id={video_response['video_id']}&notion_id={video_response['notion_id']}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail=f"Error sending video data to Notion: {response.text}")

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Error sending video data to Notion")
    
    return {
        "message": "Video generation successful",
        "video_id": video_response["video_id"],
        "notion_id": video_response["notion_id"]
        }

    