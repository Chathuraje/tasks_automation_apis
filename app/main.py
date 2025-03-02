from fastapi import FastAPI
from app.routers import root, news

app = FastAPI(
    title="Crypto Cyber News",
    description="API for Automating Crypto Cyber News Channel",
    version="1.0.0"
)

# Include routers
app.include_router(root.router)
app.include_router(news.router)