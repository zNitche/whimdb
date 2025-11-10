import asyncio
from whimdb.core import Logger, Database, Packet
from whimdb.tasks import ExpiredItemsCleanupTask
from whimdb.types import PacketTypeEnum, PacketContent
from whimdb.core import communication


class Server:
    def __init__(self, addr: str = "0.0.0.0", port: int = 8080, debug: bool = False):
        self.__debug = debug

        self.__addr = addr
        self.__port = port

        self.__events_loop = asyncio.get_event_loop()
        self.__server_mainloop = self.__get_server_mainloop()

        self.__logger = Logger(logger_name="SERVER")
        self.__logger.init(debug=self.__debug)

        self.__databases: dict[int, Database] = {}

    def __get_server_mainloop(self):
        limit_in_bytes = 5242880 # 5MB

        return asyncio.start_server(client_connected_cb=self.__client_handler,
                                    host=self.__addr, port=self.__port,
                                    reuse_port=True, reuse_address=True,
                                    limit=limit_in_bytes)

    def __register_tasks(self):
        tasks = [ExpiredItemsCleanupTask(
            dbs=self.__databases, debug=self.__debug)]

        for task in tasks:
            self.__events_loop.create_task(task.run())

            self.__logger.info(
                f"added background task: {task.__class__.__name__}")

    def __process_packet(self, packet_type: PacketTypeEnum, packet_content: PacketContent):
        database_id = packet_content.database_id

        if database_id is None:
            raise Exception(
                "error while processing packet, database_id is None")

        database_for_id = self.__databases.get(database_id)

        if not database_for_id:
            self.__databases[database_id] = Database()

        database_for_id = self.__databases[database_id]
        db_key = packet_content.key

        self.__logger.debug(
            f"got packet with type {packet_type.name} -> {packet_content}")

        match packet_type:
            case PacketTypeEnum.QUERY:
                search_regex = packet_content.search_regex

                if not db_key and not search_regex:
                    raise Exception("both key and search_regex can't be empty")

                db_items = database_for_id.query(
                    key=db_key, regex_string=search_regex)
                
                if db_items is not None:
                    db_items = [item.dump() for item in db_items]

                response_packet = Packet(type=PacketTypeEnum.RESPONSE,
                                         content=PacketContent(value=db_items))

                self.__logger.debug(f"query response: {response_packet}")

            case PacketTypeEnum.SET:
                db_value = packet_content.value

                if not db_key:
                    raise Exception("can't set None db key")

                database_for_id.set(
                    key=db_key, value=db_value, ttl=packet_content.ttl)
                response_packet = Packet(type=PacketTypeEnum.SUCCESS)

                self.__logger.debug(f"set response: {response_packet}")

            case _:
                raise Exception("unsupported packet type")

        return response_packet

    async def __client_handler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        addr = writer.get_extra_info('peername')

        try:
            self.__logger.info(f"connection from {addr}")

            packet = await communication.load_packet_from_stream(reader=reader)

            if not packet or not packet.content:
                raise Exception("Packet or its content is None")

            response_packet = self.__process_packet(
                packet_type=packet.type,
                packet_content=packet.content)

        except:
            self.__logger.exception(
                f"error while processing connection from {addr}")

            response_packet = Packet(type=PacketTypeEnum.ERROR)

        try:
            self.__logger.debug(f"sending {response_packet} to {addr}")

            writer.write(response_packet.to_bytes())
            await writer.drain()

        except:
            self.__logger.exception("error while sending packet to client")

        self.__logger.debug(f"closing connection with {addr}")

        writer.close()
        await writer.wait_closed()

        self.__logger.info(f"connection with {addr} has been closed")

    def start(self):
        self.__logger.debug("debug mode enabled")

        self.__register_tasks()
        self.__events_loop.create_task(self.__server_mainloop)

        self.__logger.info(f"running at port {self.__port}")
        self.__events_loop.run_forever()

    def stop(self):
        self.__events_loop.stop()
