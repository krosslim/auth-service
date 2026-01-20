from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TelegramInitDataPayload:
    init_data: str
