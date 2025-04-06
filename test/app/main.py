from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .google_trend_analyzer.routes.index import google_trend_analyzer_route

app = FastAPI(
    title="TESTING: Work Automation API Collection",
    description="Testing API for Automating Your Works",
    version="1.0.0",
)

# Allow CORS (Cross-Origin Resource Sharing) for docs to work
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(google_trend_analyzer_route)
