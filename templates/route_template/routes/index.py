from fastapi import APIRouter

root_router = APIRouter(
    tags=["Root"]
)

@root_router.get(
    "/", 
    summary="API Root Endpoint", 
    description="This endpoint serves as the root of API v1. It can be used for health checks or welcome messages."
)
def read_root():
    return {"message": "🚀 Welcome to the API v1"}