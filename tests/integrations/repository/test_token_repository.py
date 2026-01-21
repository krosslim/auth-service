import os
import random
from datetime import datetime, timedelta, timezone

import pytest
from dishka import Scope
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.identity_providers import AppProvider
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

            # 1. Создать пользователя и привязать один Identity: users, user_identities
            tg_id = _random_tg_id()
            user_id = await user_repo.create()
            user = await user_repo.attach_identity(provider=AppProvider.TELEGRAM, sub=str(tg_id), user_id=user_id)

            # 2. Создать токен
            token_hash = _random_bytes(32)
            expires_at = datetime.now(timezone.utc) + timedelta(days=30)

            created = await token_repo.create(
                user_id=user_id,
                token_hash=token_hash,
                expires_at=expires_at,
            )

            assert created.user_id == user_id
            assert created.token_hash == token_hash
            assert created.created_at is not None
            assert created.expires_at is not None
            assert created.revoked_at is None

            # 3. Получить токен по хэшу
            by_hash = await token_repo.get_by_hash(token_hash)
            assert by_hash is not None
            assert by_hash.user_id == user.id
            assert by_hash.token_hash == token_hash

            # 4. Сделать его просроченным
            revoked_at = datetime.now(timezone.utc)
            revoked = await token_repo.mark_revoked(
                token_hash=token_hash,
                revoked_at=revoked_at
            )
            assert revoked is not None
            assert revoked.revoked_at is not None


        finally:
            await tx.rollback()
