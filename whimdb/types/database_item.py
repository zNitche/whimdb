from typing import Any
from dataclasses import dataclass
from whimdb.types import SerializableObjectMixin


@dataclass
class DatabaseItem(SerializableObjectMixin):
    # server/client consumable
    value: Any
    created_at: int | float
    ttl: int | None

    # client consumable
    is_expired: bool | None = None
