from fastapi import APIRouter

root_router = APIRouter(
    tags=["Root"]
)

@root_router.get(
    "/",
    summary="Root Endpoint",
    description="This is the root endpoint of the API. It provides a welcome message.",
    response_model=str,
)
def read_root():
    return {"message": "🚀 Welcome to the API v1"}


@root_router.get(
    "/health",
    summary="Health Check Endpoint",
    description="This endpoint checks the health of the API. It returns a simple message indicating that the API is running.",
    response_model=str,
)
def health_check():
    return {"message": "🩺 Health Check: API is running!"}