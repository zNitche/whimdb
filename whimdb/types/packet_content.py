from typing import Any
from dataclasses import dataclass
from whimdb.types import SerializableObjectMixin


@dataclass
class PacketContent(SerializableObjectMixin):
    # server/client consumable
    key: str | None = None
    value: Any | None = None

    # server consumables
    search_regex: str | None = None
    database_id: int | None = None
    ttl: int | None = None
