from fastapi import APIRouter
from .analyzer import analyzer

google_trend_analyzer_route = APIRouter(
    prefix="/google-trend-analyzer",
    tags=["Google Trend Analyzer API"]
)

google_trend_analyzer_route.include_router(analyzer)