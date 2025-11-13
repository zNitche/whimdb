from typing import Any
from contextlib import contextmanager
import socket
import time
from whimdb.core import Packet
from whimdb.dataclasses.packet import PacketTypeEnum, PacketContent
from whimdb.dataclasses.communication import Request, ResponseDatabaseItem, Response
from whimdb.core.utils import communication, Logger


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
                self.__logger.debug(
                    f"disconnected from {self.addr}:{self.port}")

        except TimeoutError:
            raise Exception(f"connection timeout (exceeded {self.__timeout}s)")

    def query(self, key: str | None = None, search_regex: str | None = None,
              page_id: int = 0,
              items_per_page: int = 10):

        if not key and not search_regex:
            raise Exception("both key and search_regex can't be empty")

        request_content = Request(
            key=key, database_id=self.database_id, search_regex=search_regex,
            items_per_page=items_per_page, page_id=page_id)

        response_packet = self.__send_packet(packet=Packet(
            type=PacketTypeEnum.QUERY, content=PacketContent(request=request_content)))

        if not response_packet or not response_packet.content:
            return None

        response = self.__response_post_processing(
            response=response_packet.content.response)

        return response

    def set(self, key: str, value: Any | None, ttl: int | None = None):
        request_content = Request(
            key=key, database_id=self.database_id, value=value, ttl=ttl)

        packet = Packet(type=PacketTypeEnum.SET,
                        content=PacketContent(request=request_content))

        response_packet = self.__send_packet(packet=packet)

        if not response_packet:
            return False

        return response_packet.type == PacketTypeEnum.SUCCESS

    def remove(self, key: str):
        request_content = Request(key=key, database_id=self.database_id)

        packet = Packet(type=PacketTypeEnum.REMOVE,
                        content=PacketContent(request=request_content))

        response_packet = self.__send_packet(packet=packet)

        if not response_packet:
            return False

        return response_packet.type == PacketTypeEnum.SUCCESS

    def __response_post_processing(self, response: Response | None):
        if not response or not response.value:
            return None

        return Response(value=[self.__process_response_item(item) for item in response.value],
                        total_pages=response.total_pages, page_id=response.page_id)

    def __process_response_item(self, value: Any):
        item = ResponseDatabaseItem(**value)
        current_time = time.time()

        is_expired = item.ttl is not None and (
            (item.created_at + item.ttl) < current_time)

        item.is_expired = is_expired

        return item

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
