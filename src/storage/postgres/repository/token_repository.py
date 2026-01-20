from datetime import datetime
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.token import RefreshTokenDto
from src.storage.postgres.models.token import Token


class TokenRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def _to_dto(token: Token) -> RefreshTokenDto:
        return RefreshTokenDto(
            id=token.id,
            user_id=token.user_id,
            token_hash=token.token_hash,
            created_at=token.created_at,
            expires_at=token.expires_at,
            revoked_at=token.revoked_at,
            rotated_to=token.rotated_to,
        )

    async def create(
        self,
        user_id: UUID,
        token_hash: bytes,
        expires_at: datetime,
    ) -> RefreshTokenDto:
        stmt = (
            insert(Token)
            .values(
                user_id=user_id,
                token_hash=token_hash,
                expires_at=expires_at,
            )
            .returning(Token)
        )

        result = await self.session.execute(stmt)
        token: Token = result.scalar_one()
        return self._to_dto(token)

    async def get_by_id(self, token_id: UUID) -> RefreshTokenDto | None:
        stmt = select(Token).where(Token.id == token_id)
        result = await self.session.execute(stmt)
        token: Token = result.scalar_one_or_none()
        if token is None:
            return None
        return self._to_dto(token)

    async def get_by_hash(self, token_hash: bytes) -> RefreshTokenDto | None:
        stmt = select(Token).where(Token.token_hash == token_hash)
        result = await self.session.execute(stmt)
        token: Token = result.scalar_one_or_none()
        if token is None:
            return None
        return self._to_dto(token)

    async def mark_revoked(
        self,
        token_id: UUID,
        revoked_at: datetime,
        rotated_to: UUID | None = None,
    ) -> RefreshTokenDto | None:
        stmt = (
            update(Token)
            .where(Token.id == token_id)
            .values(
                revoked_at=revoked_at,
                rotated_to=rotated_to,
            )
            .returning(Token)
        )

        result = await self.session.execute(stmt)
        token: Token = result.scalar_one_or_none()
        if token is None:
            return None
        return self._to_dto(token)
