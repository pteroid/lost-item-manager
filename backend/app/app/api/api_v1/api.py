from fastapi import APIRouter

from app.api.api_v1.endpoints import admins, items, kinds, login, places, utils

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(admins.router, prefix="/admins", tags=["admins"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(places.router, prefix="/places", tags=["places"])
api_router.include_router(kinds.router, prefix="/kinds", tags=["kinds"])
