from dishka import AsyncContainer
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter
from src.api.schemas.requests import LoginRequest
from src.api.schemas.responses import AuthResponse, ErrorResponse
from src.domain.use_cases.login_use_case import LoginUseCase
from starlette import status

router = APIRouter(tags=["Login"], route_class=DishkaRoute)


@router.post(
    path="/v1/login",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
    summary="Login to your account",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid request or credentials",
            "model": ErrorResponse,
        },
        status.HTTP_409_CONFLICT: {
            "description": "Identity conflict",
            "model": ErrorResponse,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error",
            "model": ErrorResponse,
        },
    },
)
async def login(
    request: LoginRequest, container: FromDishka[AsyncContainer]
) -> AuthResponse:
    uc = await container.get(LoginUseCase, component=request.provider)
    login_data = request.model_dump(exclude={"provider"})
    result = await uc.execute(login_data)

    print(result)

    return AuthResponse.model_validate(result)
