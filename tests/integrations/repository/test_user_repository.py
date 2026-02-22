import random

import pytest
from dishka import Scope
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.identity_providers import AppProvider
from src.domain.exceptions import DuplicateIdentity, DuplicateIdentityProviderForUser
from src.ioc import container
from src.storage.database.repository.user_repository import UserRepository


@pytest.mark.integration
@pytest.mark.asyncio
async def test_user_repository_create_and_get_roundtrip():
    async with container(scope=Scope.REQUEST) as request_container:
        session = await request_container.get(AsyncSession)

        repo = UserRepository(session=session)

        tx = await session.begin()
        try:
            tg_id = random.randint(10_000_000, 2_000_000_000)

            # 1. Создаем пользователя и получаем ID
            user_id = await repo.create()
            assert user_id is not None

            # 2. Привязываем identity
            attach = await repo.attach_identity(
                provider=AppProvider.TELEGRAM,
                sub=str(tg_id),
                user_id=user_id,
            )
            assert attach is not None
            assert attach.id == user_id
            assert attach.provider == AppProvider.TELEGRAM
            assert attach.sub == str(tg_id)
            assert attach.idp_id is not None

            # 2.1. Дубль identity (provider, sub) должен дать DuplicateIdentity
            second_user_id = await repo.create()
            assert second_user_id is not None
            with pytest.raises(DuplicateIdentity):
                async with session.begin_nested():
                    await repo.attach_identity(
                        provider=AppProvider.TELEGRAM,
                        sub=str(tg_id),
                        user_id=second_user_id,
                    )

            # 2.2. Повторный provider для того же user должен дать DuplicateIdentityProviderForUser
            with pytest.raises(DuplicateIdentityProviderForUser):
                async with session.begin_nested():
                    await repo.attach_identity(
                        provider=AppProvider.TELEGRAM,
                        sub=str(tg_id + 1),
                        user_id=user_id,
                    )

            # 3. Проверяем поиск пользователя по identity
            find = await repo.find_by_identity(
                provider=AppProvider.TELEGRAM,
                sub=str(tg_id),
            )
            assert find is not None
            assert find.id == user_id
            assert find.provider == AppProvider.TELEGRAM
            assert find.sub == str(tg_id)
            assert find.idp_id == attach.idp_id


        finally:
            await tx.rollback()
