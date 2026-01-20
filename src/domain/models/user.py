from dataclasses import dataclass
from datetime import datetime
import uuid


@dataclass(slots=True)
class UserDto:
    id: uuid.UUID
    created_at: datetime
    tg_id: int | None
