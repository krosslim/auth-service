from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from src.app.config import settings as cfg


def create_engine() -> AsyncEngine:
    return create_async_engine(
        cfg.postgres.dsn,
        pool_timeout=cfg.postgres.pool_timeout,
        pool_size=cfg.postgres.pool_size,
        pool_pre_ping=cfg.postgres.pool_pre_ping,
        pool_recycle=cfg.postgres.pool_recycle,
        max_overflow=cfg.postgres.max_overflow,
        echo=cfg.postgres.echo,
    )


def build_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=engine, expire_on_commit=False)


@asynccontextmanager
async def get_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession]:
    async with session_factory() as session:
        yield session
