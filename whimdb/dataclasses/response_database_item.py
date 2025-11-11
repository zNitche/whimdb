from typing import Any
from dataclasses import dataclass
from whimdb.dataclasses import SerializableObjectMixin


@dataclass
class ResponseDatabaseItem(SerializableObjectMixin):
    value: Any
    created_at: int | float
    ttl: int | None

    is_expired: bool | None = None
