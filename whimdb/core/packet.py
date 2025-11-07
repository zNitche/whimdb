import json
from whimdb.types import PacketTypeEnum, PacketResponseContent, PacketRequestContent
from whimdb.core import communication


class Packet:
    def __init__(self, type: PacketTypeEnum,
                 response_content: PacketResponseContent | None = None,
                 request_content: PacketRequestContent | None = None):

        self.type = type
        self.__response_content = response_content
        self.__request_content = request_content

    @property
    def content(self):
        match self.type:
            case PacketTypeEnum.REQUEST:
                return self.__request_content

            case PacketTypeEnum.RESPONSE:
                return self.__response_content

            case _:
                return None

    @staticmethod
    def from_bytes(buff: bytes):
        packet_type_length = 2

        packet_type = communication.int_from_bytes(
            buff=buff[:packet_type_length])
        packet_type = PacketTypeEnum(packet_type)

        body = buff[packet_type_length:].decode()

        if packet_type == PacketTypeEnum.REQUEST:
            request_content = PacketRequestContent(**json.loads(body))
            return Packet(type=packet_type, request_content=request_content)

        elif packet_type == PacketTypeEnum.RESPONSE:
            response_content = PacketResponseContent(**json.loads(body))
            return Packet(type=packet_type, response_content=response_content)

        else:
            return Packet(type=PacketTypeEnum.ERROR)
        
    
    def to_bytes(self):
        body = self.content.dump() if self.content else {}
        
        body_buff = json.dumps(body).encode()
        type_buff = communication.int_to_bytes(self.type.value, length=2)

        content_buff = type_buff + body_buff
        size_buff = communication.int_to_bytes(val=len(content_buff))

        return size_buff + content_buff
