import socket
from whimdb.core import Logger, Packet
from whimdb.types import PacketTypeEnum, PacketContent
from whimdb.core import communication


class Client:
    def __init__(self,
                 addr: str,
                 port: int,
                 timeout: int = 2,
                 debug: bool = False):

        self.__debug = debug
        self.__timeout = timeout

        self.__logger = Logger()
        self.__logger.init(debug=self.__debug)

        self.addr = addr
        self.port = port

    def __get_socket(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.settimeout(self.__timeout)

        return soc

    @contextmanager
    def __socket_context(self):
        with self.__get_socket() as socket:
            socket.connect((self.addr, self.port))
            self.__logger.debug(f"connected to {self.addr}:{self.port}")

            yield socket

            socket.close()
            self.__logger.debug(f"disconnected from {self.addr}:{self.port}")

    def query(self, key: str, search_regex: str  | None = None):
        request_content = PacketContent(key=key, search_regex=search_regex)
        packet = Packet(type=PacketTypeEnum.REQUEST, content=request_content)

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

        return response
