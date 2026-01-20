from starlette import status
from fastapi import APIRouter

from src.api.schemas.requests import TelegramAuthRequest
from src.api.schemas.responses import AuthResponse

router = APIRouter(prefix="/v1/auth/login", tags=["Auth"])


@router.post(
    path="/telegram",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
    summary="Login to your account",
)
async def login_telegram(request: TelegramAuthRequest) -> AuthResponse: ...
