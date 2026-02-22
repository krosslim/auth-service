import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, SmallInteger, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import text
from src.storage.database.models.base import Base


class UserIdentity(Base):
    __tablename__ = "user_identities"
    __table_args__ = (
        UniqueConstraint(
            "user_id", "provider", name="user_identities_user_provider_ux"
        ),
        UniqueConstraint("provider", "sub", name="user_identities_provider_sub_ux"),
        Index("user_identities_user_id_ix", "user_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuidv7()"),
    )

    provider: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    sub: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", name="user_identities_user_id_fk"),
        nullable=False,
    )

    # --- relationships ---
    user = relationship(argument="User", back_populates="identities")
    identity_tokens = relationship(
        argument="RefreshToken", back_populates="user_identity"
    )
