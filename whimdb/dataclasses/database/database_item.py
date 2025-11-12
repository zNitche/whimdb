from typing import Any
from dataclasses import dataclass


@dataclass
class DatabaseItem:
    value: Any
    created_at: int | float
    ttl: int | None
