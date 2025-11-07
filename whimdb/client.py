import socket
from whimdb.core import Logger, Packet
from whimdb.types import PacketTypeEnum, PacketRequestContent
from whimdb.core import communication


class Client:
    def __init__(self,
                 addr: str,
                 port: int,
                 timeout: int = 2,
                 debug: bool = False):
        self.__debug = debug

        self.__logger = Logger()
        self.__logger.init(debug=self.__debug)

        self.addr = addr
        self.port = port

        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.settimeout(timeout)

    def __enter__(self):
        self.__socket.connect((self.addr, self.port))
        self.__logger.debug(f"connected to {self.addr}:{self.port}")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__socket.close()
        self.__logger.debug(f"disconnected from {self.addr}:{self.port}")

    def query(self, key: str, search_regex: str  | None = None):
        request_content = PacketRequestContent(key=key, search_regex=search_regex)
        packet = Packet(type=PacketTypeEnum.REQUEST, request_content=request_content)

        response = self.__send_packet(packet=packet)

        return response

    def __send_packet(self, packet: Packet):
        response = None

        try:
            self.__socket.sendall(packet.to_bytes())
            self.__logger.debug("packet has been sent")

            response = communication.load_packet_from_socket(socket=self.__socket)

        except:
            self.__logger.exception("error while sending packet")

        return response
