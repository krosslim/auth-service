from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession
from src.storage.database.repository.token_repository import TokenRepository
from src.storage.database.repository.user_repository import UserRepository


class RepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_user_repository(self, session: AsyncSession) -> UserRepository:
        return UserRepository(session)

    @provide(scope=Scope.REQUEST)
    def provide_token_repository(self, session: AsyncSession) -> TokenRepository:
        return TokenRepository(session)
