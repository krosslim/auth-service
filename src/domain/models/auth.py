from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TelegramAuthCredentials:
    init_data: str
