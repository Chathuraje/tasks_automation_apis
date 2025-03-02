from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.automations.crypto_cyber_news.routers import ccn_main

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
@app.get("/")
async def read_root():
    """
    Root endpoint to verify the API is running.

    - Returns a simple greeting message.
    """
    return {"message": "Hello, Crypto Cyber News!"}


app.include_router(ccn_main.router)