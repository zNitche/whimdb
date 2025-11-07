from dataclasses import dataclass


@dataclass
class PacketRequestContent:
    key: str
    search_regex: str | None

    def dump(self):
        return self.__dict__
