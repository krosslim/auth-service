from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.token import AuthResponseDto
from src.domain.providers.auth_provider import AuthProvider, UserInfo
from src.storage.postgres.repository.user_repository import UserRepository


class LoginUseCase:
    def __init__(
            self,
            provider: AuthProvider,
            session: AsyncSession,
            user_repo: UserRepository
    ):
        self.provider = provider
        self.session = session
        self.user_repo = user_repo

    async def execute(self, payload: object) -> AuthResponseDto:

        user_info = await self._authenticate(payload)




    async def _authenticate(self, payload: object) -> UserInfo:
        return await self.provider.authenticate(payload)

    async def _upsert_user(self, ):...
    'Делигировать провайдеру, так как у каждого провайдера свой ID'

