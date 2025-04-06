from fastapi import APIRouter

tools_router = APIRouter(prefix="/tools")

tools_router.include_router()