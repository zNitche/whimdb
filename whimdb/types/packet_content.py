from typing import Any
from dataclasses import dataclass


@dataclass
class PacketContent:
    value: str | None = None
    search_regex: str | None = None
    key: str | None = None

    def dump(self) -> dict[str, Any]:
        return self.__dict__
