from typing import Any
from contextlib import contextmanager
import socket
from whimdb.core import Logger, Packet
from whimdb.types import PacketTypeEnum, PacketContent
from whimdb.core import communication


class Client:
    def __init__(self,
                 database_id: int,
                 addr: str,
                 port: int,
                 timeout: int = 2,
                 debug: bool = False):

        self.__debug = debug
        self.__timeout = timeout

        self.__logger = Logger()
        self.__logger.init(debug=self.__debug)

        self.database_id = database_id

        self.addr = addr
        self.port = port

    def __get_socket(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.settimeout(self.__timeout)

        return soc

    @contextmanager
    def __socket_context(self):
        try:
            with self.__get_socket() as socket:
                socket.connect((self.addr, self.port))
                self.__logger.debug(f"connected to {self.addr}:{self.port}")

                yield socket

                socket.close()
                self.__logger.debug(f"disconnected from {self.addr}:{self.port}")
        
        except TimeoutError:
            raise Exception(f"connection timeout (exceeded {self.__timeout}s)")

    def query(self, key: str | None = None, search_regex: str | None = None):
        if not key and not search_regex:
            raise Exception("both key and search_regex can't be empty")

        request_content = PacketContent(
            key=key, database_id=self.database_id, search_regex=search_regex)
        packet = Packet(type=PacketTypeEnum.QUERY, content=request_content)

        response = self.__send_packet(packet=packet)

        return response

    def set(self, key: str, value: Any | None, ttl: int | None = None):
        request_content = PacketContent(
            key=key, database_id=self.database_id, value=value, ttl=ttl)
        packet = Packet(type=PacketTypeEnum.SET, content=request_content)

        response = self.__send_packet(packet=packet)

        return response

    def __send_packet(self, packet: Packet):
        response = None

        with self.__socket_context() as socket:
            try:
                socket.sendall(packet.to_bytes())
                self.__logger.debug("packet has been sent")

                response = communication.load_packet_from_socket(
                    socket=socket)

            except:
                self.__logger.exception("error while sending packet")

        if response and response.type == PacketTypeEnum.ERROR:
            raise Exception("received Error type packet")

        return response
