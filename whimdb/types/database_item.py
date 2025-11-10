from typing import Any
import json
from dataclasses import dataclass


@dataclass
class DatabaseItem:
    # server/client consumable
    value: Any
    created_at: int | float
    ttl: int | None

    # client consumable
    is_expired: bool | None = None

    def dump(self) -> dict[str, Any]:
        return self.__dict__
