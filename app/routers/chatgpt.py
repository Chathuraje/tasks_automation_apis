from fastapi import APIRouter, HTTPException
from app.models.news import NewsResponse
from app.services.ask_gpt import process_news_articles

# Initialize router for news-related endpoints
router = APIRouter(prefix="/chatgpt", tags=["ChatGPT"])

@router.post("/generate-script")
async def generate_news_script(news_request: NewsResponse):
    """
    Receive a list of news articles, select the best one, generate a script, and return the result.
    """
    articles = [article.dict() for article in news_request.articles]

    if not articles:
        raise HTTPException(status_code=400, detail="No articles provided.")

    processed_result = await process_news_articles(articles)

    if "error" in processed_result:
        raise HTTPException(status_code=400, detail=processed_result["error"])

    return {
        "title": processed_result["title"],
        "url": processed_result["url"],
        "script": processed_result["script"]
    }