import random

import pytest
from dishka import Scope
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.identity_providers import AppProvider
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

            # 1. Создаем пользователя и получаем ID
            user_id = await repo.create()
            assert user_id is not None

            # 2. Привязываем Identity

            attach = await repo.attach_identity(provider=AppProvider.TELEGRAM, sub=str(tg_id), user_id=user_id)
            assert attach is not None
            assert attach.provider == AppProvider.TELEGRAM
            assert attach.sub == str(tg_id)
            assert attach.id is not None

            # 2.1. Пробуем привязать дубль Identity (provider, sub) - Проверка PK. Ожидаем получить None
            second_attach = await repo.attach_identity(
                provider=AppProvider.TELEGRAM,
                sub=str(tg_id),
                user_id=user_id,
            )
            assert second_attach is None


            # 2.2. Пробуем привязать имеющийся identity к другому пользователю
            second_user_id = await repo.create()
            assert second_user_id is not None
            attach_second_user = await repo.attach_identity(
                provider=AppProvider.TELEGRAM,
                sub=str(tg_id),
                user_id=second_user_id,
            )
            assert attach_second_user is None


            # 3. Проверяем метод для получения пользователя (пользователь 1 должен быть найден)
            find = await repo.find_by_identity(provider=AppProvider.TELEGRAM, sub=str(tg_id))
            assert find is not None
            assert find.provider == AppProvider.TELEGRAM
            assert find.sub == str(tg_id)
            assert find.id == user_id

            # Пользователь 2 должен отсутствовать в БД
            find_b = await repo.find_by_identity(provider=AppProvider.TELEGRAM, sub=str(tg_id))
            assert find_b.id != second_user_id

        finally:
            await tx.rollback()
