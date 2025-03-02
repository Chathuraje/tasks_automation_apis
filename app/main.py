from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import root, news

app = FastAPI(
    title="Crypto Cyber News",
    description="API for Automating Crypto Cyber News Channel",
    version="1.0.0"
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
app.include_router(root.router)
app.include_router(news.router)