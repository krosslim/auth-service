from datetime import datetime
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.models.token import RefreshTokenDto
from src.storage.database.models.token import RefreshToken


class TokenRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def _to_dto(token: RefreshToken) -> RefreshTokenDto:
        return RefreshTokenDto(
            token_hash=token.token_hash,
            created_at=token.created_at,
            user_id=token.user_id,
            expires_at=token.expires_at,
            revoked_at=token.revoked_at,
        )

    async def create(
        self,
        user_id: UUID,
        token_hash: bytes,
        expires_at: datetime,
    ) -> RefreshTokenDto:
        stmt = (
            insert(RefreshToken)
            .values(
                user_id=user_id,
                token_hash=token_hash,
                expires_at=expires_at,
            )
            .returning(RefreshToken)
        )

        result = await self.session.execute(stmt)
        token: RefreshToken = result.scalar_one()
        return self._to_dto(token)

    async def get_by_hash(self, token_hash: bytes) -> RefreshTokenDto | None:
        stmt = select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        result = await self.session.execute(stmt)
        token: RefreshToken = result.scalar_one_or_none()
        if token is None:
            return None
        return self._to_dto(token)

    async def mark_revoked(
        self, token_hash: bytes, revoked_at: datetime
    ) -> RefreshTokenDto | None:
        stmt = (
            update(RefreshToken)
            .where(RefreshToken.token_hash == token_hash)
            .values(revoked_at=revoked_at)
            .returning(RefreshToken)
        )

        result = await self.session.execute(stmt)
        token: RefreshToken = result.scalar_one_or_none()
        if token is None:
            return None
        return self._to_dto(token)
