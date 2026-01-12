import asyncio
from whimdb.core import Database, Packet
from whimdb.tasks import ExpiredItemsCleanupTask
from whimdb.dataclasses.packet import PacketTypeEnum, PacketContent
from whimdb.dataclasses.communication import Request, QueryItem, Response
from whimdb.core.utils import communication, Logger


class Server:
    def __init__(self, addr: str = "0.0.0.0", port: int = 8080, debug: bool = False):
        self.__debug = debug

        self.__addr = addr
        self.__port = port

        self.__events_loop = self.__get_event_loop()
        self.__server_mainloop = self.__get_server_mainloop()

        self.__logger = Logger(logger_name="whimdb-server")
        self.__logger.init(debug=self.__debug)

        self.__databases: dict[int, Database] = {}

    def __get_event_loop(self):
        try:
            return asyncio.get_event_loop()
        except RuntimeError:
            asyncio.set_event_loop(asyncio.new_event_loop())

            return asyncio.get_event_loop()

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

    def __process_query_request(self, database: Database, request: Request):
        db_key = request.key
        search_regex = request.search_regex

        if not db_key and not search_regex:
            raise Exception("both key and search_regex can't be empty")

        query_response = database.query(
            key=db_key, regex_string=search_regex,
            page_id=request.page_id, items_per_page=request.items_per_page)

        response_db_items = None
        total_pages = 1
        page_id = 0

        if query_response is not None:
            response_db_items = [QueryItem.from_dict(**item.__dict__)
                                 for item in query_response.items]

            total_pages = query_response.total_pages
            page_id = query_response.page_id

        response = Response(
            value=response_db_items,
            total_pages=total_pages,
            page_id=page_id)

        return Packet(type=PacketTypeEnum.RESPONSE, content=PacketContent(response=response))

    def __process_set_request(self, database: Database, request: Request):
        db_key = request.key
        db_value = request.value

        if not db_key:
            raise Exception("can't set None db key")

        database.set(
            key=db_key, value=db_value, ttl=request.ttl)

        return Packet(type=PacketTypeEnum.SUCCESS)

    def __process_remove_request(self, database: Database, request: Request):
        db_key = request.key

        if not db_key:
            raise Exception("can't remove None db key")

        database.remove(key=db_key)

        return Packet(type=PacketTypeEnum.SUCCESS)

    def __process_purge_request(self, database: Database):
        database.purge()

        return Packet(type=PacketTypeEnum.SUCCESS)

    def __process_echo_package(self):
        return Packet(type=PacketTypeEnum.ECHO)

    def __process_update_ttl_request(self, database: Database, request: Request):
        db_key = request.key

        if not db_key:
            raise Exception("can't remove None db key")

        database.update_ttl(key=db_key, ttl=request.ttl)

        return Packet(type=PacketTypeEnum.SUCCESS)

    def __process_request(self, packet_type: PacketTypeEnum, request: Request):
        database_id = request.database_id

        if database_id is None:
            raise Exception(
                "error while processing packet, database_id is None")

        database_for_id = self.__databases.get(database_id)

        if not database_for_id:
            self.__databases[database_id] = Database()

        database_for_id = self.__databases[database_id]

        self.__logger.debug(
            f"got packet with type {packet_type.name} -> {request}")

        match packet_type:
            case PacketTypeEnum.QUERY:
                return self.__process_query_request(database=database_for_id, request=request)

            case PacketTypeEnum.SET:
                return self.__process_set_request(database=database_for_id, request=request)

            case PacketTypeEnum.REMOVE:
                return self.__process_remove_request(database=database_for_id, request=request)

            case PacketTypeEnum.PURGE:
                return self.__process_purge_request(database=database_for_id)

            case PacketTypeEnum.UPDATE_TTL:
                return self.__process_update_ttl_request(database=database_for_id,
                                                         request=request)

            case _:
                raise Exception("unsupported packet type")

    async def __client_handler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        addr = writer.get_extra_info('peername')

        try:
            self.__logger.debug(f"connection from {addr}")

            packet = await communication.load_packet_from_stream(reader=reader)

            if not packet:
                raise Exception("packet is None")

            if packet.type == PacketTypeEnum.ECHO:
                response_packet = self.__process_echo_package()

            else:
                if not packet.content or not packet.content.request:
                    raise Exception("packet's content is None")

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

        self.__logger.debug(f"connection with {addr} has been closed")

    def start(self):
        self.__logger.debug("debug mode enabled")

        self.__register_tasks()
        self.__events_loop.create_task(self.__server_mainloop)

        self.__logger.info(f"running at port {self.__port}")

        try:
            self.__events_loop.run_forever()

        except (KeyboardInterrupt, SystemExit):
            self.stop()
            self.__logger.info("exiting")

        except:
            self.stop()
            self.__logger.exception("events loop error")

    def stop(self):
        self.__events_loop.stop()
