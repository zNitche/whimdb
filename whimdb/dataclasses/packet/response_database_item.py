from typing import Any
from dataclasses import dataclass
from whimdb.dataclasses.mixins import SerializableObjectMixin


@dataclass
class ResponseDatabaseItem(SerializableObjectMixin):
    value: Any
    created_at: int | float
    ttl: int | None


    # set on client-side
    is_expired: bool | None = None
