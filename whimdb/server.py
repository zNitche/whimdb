import asyncio
from whimdb.core import Logger, Database
from whimdb.tasks import ExpiredItemsCleanupTask


class Server:
    def __init__(self, addr: str = "0.0.0.0", port: int = 8080, debug: bool = False):
        self.__debug = debug

        self.__addr = addr
        self.__port = port

        self.__events_loop = asyncio.get_event_loop()
        self.__server_mainloop = asyncio.start_server(
            self.__client_handler, self.__addr, self.__port)

        self.__logger = Logger(logger_name="SERVER")
        self.__logger.init()

        self.__databases: dict[int, Database] = {}

    def __register_tasks(self):
        tasks = [ExpiredItemsCleanupTask]

        for task in tasks:
            instance = task()
            self.__events_loop.create_task(instance.run())

            self.__logger.info(
                f"added background task: {instance.__class__.__name__}")

    async def __client_handler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        addr = writer.get_extra_info('peername')

        self.__logger.info(f"connection from {addr}")

    def run(self):
        if self.__debug:
            self.__logger.debug("debug mode enabled")

        self.__register_tasks()
        self.__events_loop.create_task(self.__server_mainloop)

        self.__logger.info(f"running at port {self.__port}")
        self.__events_loop.run_forever()

    def stop(self):
        self.__events_loop.stop()
