from collections.abc import AsyncGenerator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from src.storage.postgres.database import (
    build_session_factory,
    create_engine,
    get_session,
)


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_engine(self) -> AsyncGenerator[AsyncEngine]:
        engine = create_engine()
        try:
            yield engine
        finally:
            await engine.dispose()

    @provide(scope=Scope.APP)
    def provide_session_factory(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return build_session_factory(engine)

    @provide(scope=Scope.REQUEST)
    async def provide_db_session(
        self, session_factory: async_sessionmaker[AsyncSession]
    ) -> AsyncGenerator[AsyncSession]:
        async with get_session(session_factory) as session:
            yield session
