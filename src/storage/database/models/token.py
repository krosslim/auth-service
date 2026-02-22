from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import BYTEA, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import text
from src.storage.database.models.base import Base


class RefreshToken(Base):
    __tablename__ = "tokens"

    token_hash: Mapped[bytes] = mapped_column(BYTEA, primary_key=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", name="tokens_user_id_fk"),
        nullable=False,
    )

    idp_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("user_identities.id", name="tokens_user_idp_id_fk"),
        nullable=False,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # --- relationships ---
    user = relationship(argument="User", back_populates="tokens")
    user_identity = relationship(
        argument="UserIdentity", back_populates="identity_tokens"
    )
