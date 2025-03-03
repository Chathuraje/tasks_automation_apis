from pydantic import BaseModel
class NewsResponse(BaseModel):
    title: str
    url: str
    script: str
    seo_title: str
    seo_description: str
    seo_tags: list[str]
    image_prompt: str


class NewsScrape(BaseModel):
    title: str
    url: str

class VideoData(BaseModel):
    notion_id: str
    folder_id: str
    

    
    