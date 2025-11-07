
from dataclasses import dataclass


@dataclass
class PacketResponseContent:
    value: str

    def dump(self):
        return self.__dict__
