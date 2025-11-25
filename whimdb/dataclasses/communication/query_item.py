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
    ttl_left: int | None = None

    @staticmethod
    def get_defaults():
        return {
            "key": None,
            "value": None,
            "created_at": None,
            "ttl": None,
            "is_expired": None,
            "ttl_left": None,
        }
