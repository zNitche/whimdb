from dataclasses import dataclass
from typing import Any
from whimdb.dataclasses.mixins import SerializableObjectMixin
from whimdb.dataclasses.communication import QueryItem


@dataclass
class Response(SerializableObjectMixin):
    value: list[QueryItem] | None
    total_pages: int | None = None
    page_id: int | None = None

    @staticmethod
    def get_defaults():
        return {
            "value": None,
            "total_pages": None,
            "page_id": None
        }

    def dump(self) -> dict[str, Any]:
        return {
            "value": [item.dump() for item in self.value] if self.value else None,
            "total_pages": self.total_pages,
            "page_id": self.page_id
        }
