import uuid
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import text
from src.storage.postgres.models.base import Base


class User(Base):
    __tablename__ = "users"

    __table_args__ = (UniqueConstraint("tg_id", name="uq_users_tg_id"),)

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, server_default=text("uuidv7()")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )
    tg_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    # --- relationships ---

    tokens = relationship("Token", back_populates="user")
