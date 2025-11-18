from dataclasses import dataclass
from whimdb.dataclasses.mixins import SerializableObjectMixin


@dataclass
class QueryItem(SerializableObjectMixin):
    key: str
    value: str
    created_at: int | float
    ttl: int | None


    # set on client-side
    is_expired: bool | None = None
