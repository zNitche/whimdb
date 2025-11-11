from typing import Any
from dataclasses import dataclass


@dataclass
class SerializableObjectMixin:
    def dump(self) -> dict[str, Any]:
        return self.__dict__
    
    def __str__(self) -> str:
        return str(self.__dict__)
