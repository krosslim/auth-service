from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.models.user import UserDto
from src.storage.postgres.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def _to_dto(user: User) -> UserDto:
        return UserDto(
            id=user.id,
            created_at=user.created_at,
            tg_id=user.tg_id,
        )

    async def create_from_tg_id(self, tg_id: int) -> UserDto:
        stmt = (
            insert(User)
            .values(tg_id=tg_id)
            .on_conflict_do_nothing(index_elements=[User.tg_id])
            .returning(User)
        )

        result = await self.session.execute(stmt)
        user: User = result.scalar_one_or_none()
        if user is None:
            return await self.get_by_tg_id(tg_id)

        return self._to_dto(user)

    async def get_by_tg_id(self, tg_id: int) -> UserDto | None:
        stmt = select(User).where(User.tg_id == tg_id)
        result = await self.session.execute(stmt)
        user: User = result.scalar_one_or_none()
        if user is None:
            return None
        return self._to_dto(user)

    async def get_by_id(self, user_id: UUID) -> UserDto | None:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        user: User = result.scalar_one_or_none()
        if user is None:
            return None
        return self._to_dto(user)
