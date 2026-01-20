from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True, frozen=True)
class RefreshTokenDto:
    id: UUID
    user_id: UUID
    token_hash: bytes
    created_at: datetime
    expires_at: datetime
    revoked_at: datetime = None
    rotated_to: UUID = None
