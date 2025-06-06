from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.main import v1_router

app = FastAPI(
    title="Work Automation API Collection",
    description="API for Automating Your Works",
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
app.include_router(v1_router)
