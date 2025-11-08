from enum import Enum


class PacketTypeEnum(Enum):
    ERROR = 0
    SUCCESS = 1
    QUERY = 2
    SET = 3
    RESPONSE = 4
