from pydantic import BaseModel
class NewsResponse(BaseModel):
    article_title: str
    article_url: str
    script: str
    seo_title: str
    seo_description: str
    seo_tags: list[str]
