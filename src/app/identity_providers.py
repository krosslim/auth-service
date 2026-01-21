from enum import IntEnum
from typing import Any, Self


class AppProvider(IntEnum):
    """
    Все доступные Identity Providers в сервисе.
    Менять порядок значений запрещено.
    """

    TELEGRAM = 0

    def __str__(self) -> str:
        return self.name.lower()

    @classmethod
    def _missing_(cls: type[Self], value: Any) -> "AppProvider":
        if isinstance(value, str):
            try:
                return cls[value.upper()]
            except KeyError:
                pass
        raise ValueError(f"Unknown app provider: {value!r}")
