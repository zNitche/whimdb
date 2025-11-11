from dataclasses import dataclass
from typing import Any
from whimdb.dataclasses import SerializableObjectMixin, ResponseDatabaseItem


@dataclass
class Response(SerializableObjectMixin):
    value: list[ResponseDatabaseItem] | None

    def dump(self) -> dict[str, Any]:
        return {
            "value": [item.dump() for item in self.value] if self.value else None
        }
