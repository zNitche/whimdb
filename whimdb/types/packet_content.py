from typing import Any
from dataclasses import dataclass


@dataclass
class PacketContent:
    # server/client consumable
    key: str | None = None
    value: Any | None = None

    # server consumables
    search_regex: str | None = None
    database_id: int | None = None
    ttl: int | None = None

    def dump(self) -> dict[str, Any]:
        return self.__dict__
    
    def __str__(self) -> str:
        return str(self.__dict__)
