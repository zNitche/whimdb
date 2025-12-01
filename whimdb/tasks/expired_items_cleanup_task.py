import asyncio
import time
from whimdb.tasks import TaskBase
from whimdb.core import Database


class ExpiredItemsCleanupTask(TaskBase):
    def __init__(self, dbs: dict[int, Database], debug: bool = False):
        super().__init__(debug=debug)

        self.__dbs = dbs

    async def run(self):
        while True:
            for db_id in self.__dbs:
                keys_to_remove: list[str] = []

                db = self.__dbs[db_id]
                db_content = db.content

                for key in db_content:
                    db_item = db_content[key]

                    valid_till = db_item.valid_till

                    if valid_till is not None:
                        if valid_till < time.time():
                            keys_to_remove.append(key) 

                for key in keys_to_remove:
                    db.remove(key=key)

                removed_count = len(keys_to_remove)

                if removed_count > 0:
                    self._logger.info(
                        f"done, removed {removed_count} items from db:{db_id}")

            await asyncio.sleep(10)
