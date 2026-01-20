from abc import ABC, abstractmethod

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class UserInfo:
    provider: str
    sub: str


class AuthProvider(ABC):
    @abstractmethod
    async def authenticate(self, payload: object) -> UserInfo: ...
