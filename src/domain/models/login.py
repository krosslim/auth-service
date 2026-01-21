from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TelegramLoginCredentials:
    init_data: str
