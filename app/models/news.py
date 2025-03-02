from pydantic import BaseModel
from typing import Optional

class NewsArticle(BaseModel):
    author: Optional[str]
    title: str
    description: Optional[str]
    publishedAt: str
    url: str

class NewsResponse(BaseModel):
    status: str
    totalResults: int
    articles: list[NewsArticle]
