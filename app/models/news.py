from pydantic import BaseModel
from typing import Optional

class NewsArticle(BaseModel):
    title: str
    url: str

class NewsResponse(BaseModel):
    articles: list[NewsArticle]
