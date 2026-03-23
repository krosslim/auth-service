from fastapi import APIRouter

from .auth import router as auth_router
from .token import router as token_router

api_router_v1 = APIRouter(prefix="/v1")

api_router_v1.include_router(auth_router)
api_router_v1.include_router(token_router)
