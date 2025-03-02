from fastapi import APIRouter

# Initialize router
router = APIRouter()

@router.get("/")
async def read_root():
    """
    Root endpoint to verify the API is running.

    - Returns a simple greeting message.
    """
    return {"message": "Hello, Crypto Cyber News!"}
