from whimdb.core.packet import Packet
from tests import mocks


def test_load_packet():
    packet = Packet.from_bytes(mocks.PACKET_BUFF)

    assert packet.type == mocks.PACKET.type
    assert packet.content == mocks.PACKET.content


def test_dump_packet():
    packet_buff = mocks.PACKET.to_bytes()

    assert packet_buff == mocks.PACKET_RAW_BUFF
