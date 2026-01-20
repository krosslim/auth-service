import os
import random
from datetime import datetime, timedelta, timezone

import pytest
from dishka import Scope
from sqlalchemy.ext.asyncio import AsyncSession

from src.ioc import container
from src.storage.postgres.repository.user_repository import UserRepository
from src.storage.postgres.repository.token_repository import TokenRepository


def _random_bytes(n: int = 32) -> bytes:
    return os.urandom(n)


def _random_tg_id() -> int:
    return random.randint(10_000_000, 2_000_000_000)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_token_repository_create_and_get_roundtrip():
    async with container(scope=Scope.REQUEST) as request_container:
        session = await request_container.get(AsyncSession)

        user_repo = UserRepository(session=session)
        token_repo = TokenRepository(session=session)

        tx = await session.begin()
        try:
            tg_id = _random_tg_id()
            user = await user_repo.create_from_tg_id(tg_id)

            token_hash = _random_bytes(32)
            expires_at = datetime.now(timezone.utc) + timedelta(days=30)

            created = await token_repo.create(
                user_id=user.id,
                token_hash=token_hash,
                expires_at=expires_at,
            )

            assert created.id is not None
            assert created.user_id == user.id
            assert created.token_hash == token_hash
            assert created.created_at is not None
            assert created.expires_at is not None
            assert created.revoked_at is None
            assert created.rotated_to is None

            by_hash = await token_repo.get_by_hash(token_hash)
            assert by_hash is not None
            assert by_hash.id == created.id
            assert by_hash.user_id == user.id
            assert by_hash.token_hash == token_hash

            by_id = await token_repo.get_by_id(created.id)
            assert by_id is not None
            assert by_id.id == created.id
            assert by_id.user_id == user.id
            assert by_id.token_hash == token_hash
        finally:
            await tx.rollback()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_token_repository_revoke_roundtrip():
    async with container(scope=Scope.REQUEST) as request_container:
        session = await request_container.get(AsyncSession)

        user_repo = UserRepository(session=session)
        token_repo = TokenRepository(session=session)

        tx = await session.begin()
        try:
            tg_id = _random_tg_id()
            user = await user_repo.create_from_tg_id(tg_id)

            token_hash = _random_bytes(32)
            expires_at = datetime.now(timezone.utc) + timedelta(days=30)

            created = await token_repo.create(
                user_id=user.id,
                token_hash=token_hash,
                expires_at=expires_at,
            )
            assert created.revoked_at is None

            revoked_at = datetime.now(timezone.utc)

            revoked = await token_repo.mark_revoked(
                token_id=created.id,
                revoked_at=revoked_at,
                rotated_to=None,
            )
            assert revoked is not None
            assert revoked.id == created.id
            assert revoked.revoked_at is not None

            by_id = await token_repo.get_by_id(created.id)
            assert by_id is not None
            assert by_id.id == created.id
            assert by_id.revoked_at is not None
        finally:
            await tx.rollback()
