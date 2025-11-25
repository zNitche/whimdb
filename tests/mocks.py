from whimdb.dataclasses.packet import PacketContent, PacketTypeEnum
from whimdb.dataclasses.communication import Request
from whimdb.core import Packet


PACKET_BUFF = b'\x00\x04{"response": null, "request": {"database_id": 0, "key": "test_key", "value": "test_value", "page_id": 0}}'
PACKET_RAW_BUFF = b'\x00\x00\x00k' + PACKET_BUFF
PACKET = Packet(type=PacketTypeEnum.SET,
                content=PacketContent(request=Request(database_id=0, key="test_key", value="test_value", page_id=0)))
