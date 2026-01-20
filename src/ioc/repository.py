from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from src.storage.postgres.repository.user_repository import UserRepository
from src.storage.postgres.repository.token_repository import TokenRepository


class RepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_user_repository(self, session: AsyncSession) -> UserRepository:
        return UserRepository(session)

    @provide(scope=Scope.REQUEST)
    def provide_token_repository(self, session: AsyncSession) -> TokenRepository:
        return TokenRepository(session)
