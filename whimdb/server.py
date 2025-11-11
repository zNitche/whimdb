import asyncio
from whimdb.core import Logger, Database, Packet
from whimdb.tasks import ExpiredItemsCleanupTask
from whimdb.dataclasses import PacketTypeEnum, PacketContent, Request, Response, ResponseDatabaseItem
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
        limit_in_bytes = 5242880  # 5MB

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

    def __process_request(self, packet_type: PacketTypeEnum, request: Request):
        response_packet_type = PacketTypeEnum.ERROR
        response_packet_reponse = None

        database_id = request.database_id

        if database_id is None:
            raise Exception(
                "error while processing packet, database_id is None")

        database_for_id = self.__databases.get(database_id)

        if not database_for_id:
            self.__databases[database_id] = Database()

        database_for_id = self.__databases[database_id]
        db_key = request.key

        self.__logger.debug(
            f"got packet with type {packet_type.name} -> {request}")

        match packet_type:
            case PacketTypeEnum.QUERY:
                search_regex = request.search_regex

                if not db_key and not search_regex:
                    raise Exception("both key and search_regex can't be empty")

                db_items = database_for_id.query(
                    key=db_key, regex_string=search_regex)

                response_db_items = None

                if db_items is not None:
                    response_db_items = [ResponseDatabaseItem(
                        **item.__dict__) for item in db_items]

                response_packet_type = PacketTypeEnum.RESPONSE
                response_packet_reponse = Response(value=response_db_items)

            case PacketTypeEnum.SET:
                db_value = request.value

                if not db_key:
                    raise Exception("can't set None db key")

                database_for_id.set(
                    key=db_key, value=db_value, ttl=request.ttl)

                response_packet_type = PacketTypeEnum.SUCCESS

            case _:
                raise Exception("unsupported packet type")

        response_packet = Packet(type=response_packet_type, content=PacketContent(
            response=response_packet_reponse))

        self.__logger.debug(f"response: {response_packet}")

        return response_packet

    async def __client_handler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        addr = writer.get_extra_info('peername')

        try:
            self.__logger.info(f"connection from {addr}")

            packet = await communication.load_packet_from_stream(reader=reader)

            if not packet or not packet.content or not packet.content.request:
                raise Exception("Packet or its content is None")

            response_packet = self.__process_request(
                packet_type=packet.type,
                request=packet.content.request)

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
