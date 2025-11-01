import asyncio
from whimdb.tasks import ExpiredItemsCleanupTask


class Server:
    def __init__(self):
        self.__events_loop = asyncio.get_event_loop()

    def __register_tasks(self):
        tasks = [ExpiredItemsCleanupTask]

        for task in tasks:
            instance = task()
            self.__events_loop.create_task(instance.run())


    def run(self):
        self.__register_tasks()

        self.__events_loop.run_forever()

    def stop(self):
        self.__events_loop.stop()
