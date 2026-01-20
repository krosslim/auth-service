from uuid import UUID
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import BYTEA, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import text
from src.storage.postgres.models.base import Base


class Token(Base):
    __tablename__ = "tokens"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, server_default=text("uuidv7()")
    )

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )

    token_hash: Mapped[bytes] = mapped_column(BYTEA, nullable=False, unique=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    rotated_to: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("tokens.id"), nullable=True
    )

    # --- relationships ---

    user = relationship(
        "User",
        back_populates="tokens",
    )

    rotated_token = relationship(
        "Token",
        foreign_keys="Token.rotated_to",
        remote_side="Token.id",
        uselist=False,
    )
