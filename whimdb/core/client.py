import socket
from whimdb import Logger


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
