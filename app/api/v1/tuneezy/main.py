from fastapi import APIRouter
from .video_generation.routes.index import video_generation

tuneezy_router = APIRouter(
    prefix="/tuneezy",
    tags=["Tuneezy Youtube Automations"],
    responses={404: {"description": "Not found"}},
)

tuneezy_router.include_router(video_generation)
