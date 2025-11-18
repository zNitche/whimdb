from enum import Enum


class PacketTypeEnum(Enum):
    ECHO = 0
    ERROR = 1
    SUCCESS = 2
    QUERY = 3
    SET = 4
    RESPONSE = 5
    REMOVE = 6
    PURGE = 7
    UPDATE_TTL = 8
