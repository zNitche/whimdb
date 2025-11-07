import asyncio
import socket


def int_to_bytes(val: int, length: int = 4):
    return val.to_bytes(length, byteorder="big")


def int_from_bytes(buff: bytes):
    return int.from_bytes(buff, byteorder="big")


async def read_from_stream(reader: asyncio.StreamReader, length: int,
                           raise_exception: bool = True, timeout: float = 1) -> bytes:

    data = await asyncio.wait_for(reader.read(length), timeout=timeout)

    if raise_exception and (len(data) < length):
        raise Exception(
            f"receive length missmatch, requested {length}, got {len(data)}")

    return data


def read_from_socket(socket: socket.socket, length: int,
                     raise_exception: bool = True) -> bytes:

    data = socket.recv(length)

    if raise_exception and (len(data) < length):
        raise Exception(
            f"receive length missmatch, requested {length}, got {len(data)}")

    return data


def load_packet_from_socket(socket: socket.socket):
    from whimdb.core import Packet

    size_buffer = read_from_socket(socket=socket, length=4)
    size = int_from_bytes(size_buffer)

    if not size:
        return None

    data = read_from_socket(socket=socket, length=size)

    return Packet.from_bytes(buff=data)


async def load_packet_from_stream(reader: asyncio.StreamReader):
    from whimdb.core import Packet

    size_buffer = await read_from_stream(reader=reader, length=4)
    size = int_from_bytes(size_buffer)

    if not size:
        return None

    data = await read_from_stream(reader=reader, length=size)

    return Packet.from_bytes(buff=data)
