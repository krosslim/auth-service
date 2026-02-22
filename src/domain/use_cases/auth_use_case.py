from sqlalchemy.ext.asyncio import AsyncSession
from src.app.identity_providers import AppProvider
from src.domain.models.token import AuthResponseDto
from src.domain.providers.auth_provider import AuthProvider
from src.domain.use_cases.token_use_case import TokenUseCase
from src.storage.database.repository.user_repository import UserRepository


class AuthUseCase:
    def __init__(
        self,
        provider: AuthProvider,
        session: AsyncSession,
        user_repo: UserRepository,
        token: TokenUseCase,
    ):
        self.provider = provider
        self.session = session
        self.user_repo = user_repo
        self.token = token

    async def execute(self, payload: dict) -> AuthResponseDto:
        async with self.session.begin():
            credentials = await self.provider.authenticate(payload)

            user = await self.user_repo.find_by_identity(
                provider=AppProvider(credentials.provider), sub=credentials.sub
            )

            if not user:
                user_id = await self.user_repo.create()
                user = await self.user_repo.attach_identity(
                    provider=AppProvider(credentials.provider),
                    sub=credentials.sub,
                    user_id=user_id,
                )

            token_pair = await self.token.issue(user.id, user.idp_id)

        return token_pair
