from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.identity_providers import AppProvider
from src.domain.models.user import UserDto
from src.storage.database.models import UserIdentity
from src.storage.database.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def _to_dto(user: UserIdentity) -> UserDto:
        return UserDto(
            id=user.user_id, provider=AppProvider(user.provider), sub=user.sub
        )

    async def create(self) -> UUID:
        stmt = insert(User).returning(User.id)

        result = await self.session.execute(stmt)
        user_id = result.scalar_one()

        return user_id

    async def attach_identity(
        self, provider: AppProvider, sub: str, user_id: UUID
    ) -> UserDto:
        stmt = (
            insert(UserIdentity)
            .values(provider=provider, sub=sub, user_id=user_id)
            .on_conflict_do_nothing(
                index_elements=[UserIdentity.provider, UserIdentity.sub]
            )
            .returning(UserIdentity)
        )
        result = await self.session.execute(stmt)
        user: UserIdentity = result.scalar_one_or_none()
        if user is not None:
            return self._to_dto(user)
        # обработка race condition
        return await self.find_by_identity(provider, sub)

    async def find_by_identity(self, provider: AppProvider, sub: str) -> UserDto | None:
        stmt = select(UserIdentity).where(
            UserIdentity.provider == provider, UserIdentity.sub == sub
        )
        result = await self.session.execute(stmt)
        user: UserIdentity = result.scalar_one_or_none()
        if user is None:
            return None
        return self._to_dto(user)
