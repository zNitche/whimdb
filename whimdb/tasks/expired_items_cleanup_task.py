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
            current_time = time.time()

            for db_id in self.__dbs:
                keys_to_remove: list[str] = []
                db_content = self.__dbs[db_id].content

                for key in db_content:
                    db_item = db_content[key]

                    ttl = db_item.ttl
                    created_at = db_item.created_at

                    if ttl is not None and ((created_at + ttl) < current_time):
                        keys_to_remove.append(key)

                for key in keys_to_remove:
                    del db_content[key]

                removed_count = len(keys_to_remove)

                if removed_count > 0:
                    self._logger.info(f"done, removed {removed_count} items from db id:{db_id}")

            await asyncio.sleep(10)
