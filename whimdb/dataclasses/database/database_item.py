from dataclasses import dataclass


@dataclass
class DatabaseItem:
    key: str
    value: str | int | bool | dict | None
    created_at: int | float
    valid_till: int | float | None
