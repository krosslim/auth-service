from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter
from src.api.schemas.requests import RefreshTokenRequest
from src.api.schemas.responses import AuthResponse, ErrorResponse
from src.domain.use_cases.token_use_case import TokenUseCase
from starlette import status

router = APIRouter(tags=["Token"], route_class=DishkaRoute)


@router.post(
    path="/v1/refresh",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
    summary="Login to your account",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid request or credentials",
            "model": ErrorResponse,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized",
            "model": ErrorResponse,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error",
            "model": ErrorResponse,
        },
    },
)
async def refresh(
    request: RefreshTokenRequest, uc: FromDishka[TokenUseCase]
) -> AuthResponse:
    result = await uc.refresh(request.refresh_token)

    return AuthResponse.model_validate(result)


@router.post(
    path="/v1/revoke",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Login to your account",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid request or credentials",
            "model": ErrorResponse,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized",
            "model": ErrorResponse,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error",
            "model": ErrorResponse,
        },
    },
)
async def revoke(request: RefreshTokenRequest, uc: FromDishka[TokenUseCase]) -> None:
    await uc.revoke(request.refresh_token)
    return None
