from fastapi import APIRouter

from .v1 import api_router_v1

api_router = APIRouter()

api_router.include_router(api_router_v1)
