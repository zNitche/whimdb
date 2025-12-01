from typing import Any
from dataclasses import dataclass


@dataclass
class DatabaseItem:
    key: str
    value: Any
    created_at: int | float
    valid_till: int | float | None
