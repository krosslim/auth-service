from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.identity_providers import AppProvider
from src.domain.exceptions import DuplicateIdentityException
from src.domain.models.token import AuthResponseDto
from src.domain.models.user import UserDto
from src.domain.providers.auth_provider import AuthProvider, UserInfo
from src.storage.database.repository.user_repository import UserRepository


class LoginUseCase:
    def __init__(
        self, provider: AuthProvider, session: AsyncSession, user_repo: UserRepository
    ):
        self.provider = provider
        self.session = session
        self.user_repo = user_repo

    async def execute(self, payload: dict) -> AuthResponseDto:
        async with self.session.begin():
            credentials = await self._authenticate(payload)

            user = await self._get_user_by_identity(
                provider=AppProvider(credentials.provider), sub=credentials.sub
            )

            if not user:
                user_id = await self._create_user()
                try:
                    user = await self._attach_user_identity(
                        provider=AppProvider(credentials.provider),
                        sub=credentials.sub,
                        user_id=user_id,
                    )
                except IntegrityError:
                    raise DuplicateIdentityException(
                        code="DUPLICATE_IDENTITY_PROVIDER",
                        message="This identity provider is already linked to the user",
                    )

        # TO DO: Создать refresh/access токены

        return AuthResponseDto(access_token="test", refresh_token="test")

    async def _authenticate(self, payload: dict) -> UserInfo:
        return await self.provider.authenticate(payload)

    async def _get_user_by_identity(
        self, provider: AppProvider, sub: str
    ) -> UserDto | None:
        return await self.user_repo.find_by_identity(provider, sub)

    async def _create_user(self) -> UUID:
        return await self.user_repo.create()

    async def _attach_user_identity(
        self, provider: AppProvider, sub: str, user_id: UUID
    ) -> UserDto | None:
        return await self.user_repo.attach_identity(provider, sub, user_id)
