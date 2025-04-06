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
