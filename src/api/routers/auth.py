from dishka import AsyncContainer
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter
from src.api.schemas.requests import AuthRequest
from src.api.schemas.responses import COMMON_RESPONSES, AuthResponse
from src.domain.use_cases.auth_use_case import AuthUseCase
from starlette import status

router = APIRouter(tags=["Auth"], route_class=DishkaRoute)


@router.post(
    path="/v1/auth",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate by app providers",
    responses=COMMON_RESPONSES,
)
async def authenticate(
    request: AuthRequest, container: FromDishka[AsyncContainer]
) -> AuthResponse:
    uc = await container.get(AuthUseCase, component=request.provider)
    auth_data = request.model_dump(exclude={"provider"})
    result = await uc.execute(auth_data)

    return AuthResponse.model_validate(result)
