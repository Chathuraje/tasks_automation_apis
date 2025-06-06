from fastapi import APIRouter
from .ffmpeg.routes.index import ffmpeg_router

tools_router = APIRouter(prefix="/tools")

tools_router.include_router(ffmpeg_router)
