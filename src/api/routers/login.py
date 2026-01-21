from dishka import AsyncContainer
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter
from src.api.schemas.requests import LoginRequest
from src.api.schemas.responses import AuthResponse
from src.domain.use_cases.login_use_case import LoginUseCase
from starlette import status

router = APIRouter(prefix="/login", tags=["Login"], route_class=DishkaRoute)


@router.post(
    path="/login",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
    summary="Login to your account",
)
async def login(
    request: LoginRequest, container: FromDishka[AsyncContainer]
) -> AuthResponse:
    uc = await container.get(LoginUseCase, component=request.provider)
    login_data = request.model_dump(exclude={"provider"})
    result = await uc.execute(login_data)

    print(result)

    return AuthResponse.model_validate(result)
