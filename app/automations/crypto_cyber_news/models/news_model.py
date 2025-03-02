from pydantic import BaseModel
class NewsResponse(BaseModel):
    title: str
    url: str
    script: str
    seo_title: str
    seo_description: str
    seo_tags: list[str]
    image_prompts: list[str]


class NewsScrape(BaseModel):
    title: str
    url: str
    
class NewsScrapeResponse(BaseModel):
    count: int
    articles: list[NewsScrape]
    
    

    
    