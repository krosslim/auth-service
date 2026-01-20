from typing import Annotated

from fastapi import APIRouter
from src.api.schemas.requests import TelegramAuthRequest
from src.api.schemas.responses import AuthResponse
from starlette import status

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from dishka import FromComponent

from src.domain.models.telegram import TelegramInitDataPayload
from src.domain.use_cases.login_use_case import LoginUseCase

router = APIRouter(prefix="/login", tags=["Login"], route_class=DishkaRoute)


@router.post(
    path="/telegram",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
    summary="Login to your account",
)
async def login_telegram(
        request: TelegramAuthRequest,
        uc: FromDishka[Annotated[LoginUseCase, FromComponent("telegram")]]
) -> AuthResponse:

    dto = TelegramInitDataPayload(
        init_data=request.init_data
    )


