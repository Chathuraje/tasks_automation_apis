from fastapi import APIRouter
from .root.routes.index import root_router
from .tools.main import tools_router
from .tuneezy.main import tuneezy_router

v1_router = APIRouter(prefix="/api/v1")

v1_router.include_router(root_router)
v1_router.include_router(tuneezy_router)
v1_router.include_router(tools_router)
