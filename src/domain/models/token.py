from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True, frozen=True)
class RefreshTokenDto:
    token_hash: bytes
    created_at: datetime
    user_id: UUID
    expires_at: datetime
    revoked_at: datetime = None


@dataclass(slots=True, frozen=True)
class AuthResponseDto:
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
