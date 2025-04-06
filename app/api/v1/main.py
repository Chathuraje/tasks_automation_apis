from fastapi import APIRouter
from .root.routes.index import root_router

v1_router = APIRouter(prefix="/api/v1")

v1_router.include_router(root_router)