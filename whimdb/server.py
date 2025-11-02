import asyncio
from whimdb.core import Logger, Database
from whimdb.tasks import ExpiredItemsCleanupTask


class Server:
    def __init__(self, port: int):
        self.__port = port

        self.__events_loop = asyncio.get_event_loop()
        self.__server_mainloop = asyncio.start_server(
            self.__client_handler, "0.0.0.0", self.__port)
        
        self.__logger = Logger(logger_name="SERVER")
        self.__logger.init()

        self.__databases: dict[int, Database] = {}

    def __register_tasks(self):
        tasks = [ExpiredItemsCleanupTask]

        for task in tasks:
            instance = task()
            self.__events_loop.create_task(instance.run())

    async def __client_handler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        addr = writer.get_extra_info('peername')

        self.__logger.info(f"connection from {addr}")

    def run(self):
        self.__register_tasks()
        self.__events_loop.create_task(self.__server_mainloop)
        
        self.__logger.info(f"running at port {self.__port}")
        self.__events_loop.run_forever()

    def stop(self):
        self.__events_loop.stop()
