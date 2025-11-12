from typing import Any
from dataclasses import dataclass
from whimdb.dataclasses.mixins import SerializableObjectMixin


@dataclass
class Request(SerializableObjectMixin):
    database_id: int
    key: str | None = None
    value: Any = None
    search_regex: str | None = None
    ttl: int | None = None
    items_per_page: int = 20
    page_id: int = 0
