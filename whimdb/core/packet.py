import json
from whimdb.types import PacketTypeEnum, PacketContent
from whimdb.core import communication


class Packet:
    def __init__(self, type: PacketTypeEnum,
                 content: PacketContent | None = None):

        self.type = type
        self.content = content

    @staticmethod
    def from_bytes(buff: bytes):
        packet_type_length = 2

        packet_type = communication.int_from_bytes(
            buff=buff[:packet_type_length])
        packet_type = PacketTypeEnum(packet_type)

        body = buff[packet_type_length:].decode()

        packet_content = PacketContent(**json.loads(body))
        return Packet(type=packet_type, content=packet_content)
        
    
    def to_bytes(self):
        body = self.content.dump() if self.content else {}
        
        body_buff = json.dumps(body).encode()
        type_buff = communication.int_to_bytes(self.type.value, length=2)

        content_buff = type_buff + body_buff
        size_buff = communication.int_to_bytes(val=len(content_buff), length=2)

        return size_buff + content_buff
    
    def __str__(self):
        return f"{self.type.name}/{self.content}"
