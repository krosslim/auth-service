import uuid
from dataclasses import dataclass

from src.app.identity_providers import AppProvider


@dataclass(slots=True, frozen=True)
class UserDto:
    id: uuid.UUID
    provider: AppProvider
    sub: str
