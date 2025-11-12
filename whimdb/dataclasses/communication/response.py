from dataclasses import dataclass
from typing import Any
from whimdb.dataclasses.mixins import SerializableObjectMixin
from whimdb.dataclasses.communication import ResponseDatabaseItem


@dataclass
class Response(SerializableObjectMixin):
    value: list[ResponseDatabaseItem] | None
    total_pages: int = 1
    page_id: int = 0

    def dump(self) -> dict[str, Any]:
        return {
            "value": [item.dump() for item in self.value] if self.value else None,
            "total_pages": self.total_pages,
            "page_id": self.page_id
        }
