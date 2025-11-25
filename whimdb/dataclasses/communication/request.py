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
    items_per_page: int | None = None
    page_id: int | None = None

    @staticmethod
    def get_defaults():
        return {
            "database_id": None,
            "key": None,
            "value": None,
            "search_regex": None,
            "ttl": None,
            "items_per_page": None,
            "page_id": None,
        }
