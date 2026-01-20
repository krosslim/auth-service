import random

import pytest
from dishka import Scope
from sqlalchemy.ext.asyncio import AsyncSession

from src.ioc import container
from src.storage.postgres.repository.user_repository import UserRepository


@pytest.mark.integration
@pytest.mark.asyncio
async def test_user_repository_create_and_get_roundtrip():
    async with container(scope=Scope.REQUEST) as request_container:
        session = await request_container.get(AsyncSession)

        repo = UserRepository(session=session)

        tx = await session.begin()
        try:
            tg_id = random.randint(10_000_000, 2_000_000_000)

            created = await repo.create_from_tg_id(tg_id)
            assert created.tg_id == tg_id
            assert created.id is not None
            assert created.created_at is not None

            by_tg = await repo.get_by_tg_id(tg_id)
            assert by_tg.id == created.id
            assert by_tg.tg_id == tg_id

            by_id = await repo.get_by_id(created.id)
            assert by_id.id == created.id
            assert by_id.tg_id == tg_id
        finally:
            await tx.rollback()
