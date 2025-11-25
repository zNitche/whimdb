from typing import Any
import copy
from dataclasses import dataclass


@dataclass
class SerializableObjectMixin:
    def dump(self) -> dict[str, Any]:
        d = {}

        for key, value in self.__dict__.items():
            if value is not None:
                d[key] = value

        return d
    
    @staticmethod
    def get_defaults():
        raise NotImplementedError()
    
    @classmethod
    def load(cls, **kwargs):
        target_kwargs = {}
        inital_dict = cls.get_defaults()

        for key in inital_dict:
            if key not in kwargs.keys():
                target_kwargs[key] = None

        for key, value in kwargs.items():
            target_kwargs[key] = value

        return cls(**target_kwargs)

    
    def __str__(self) -> str:
        return str(self.__dict__)
