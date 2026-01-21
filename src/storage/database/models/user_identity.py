import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, SmallInteger, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import text
from src.storage.database.models.base import Base


class UserIdentity(Base):
    __tablename__ = "user_identities"
    __table_args__ = (
        Index(
            "user_identities_user_provider_ux",
            "user_id",
            "provider",
            unique=True,
        ),
    )

    provider: Mapped[int] = mapped_column(
        SmallInteger, primary_key=True, nullable=False
    )
    sub: Mapped[str] = mapped_column(Text, primary_key=True, nullable=False)

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
