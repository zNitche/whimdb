import asyncio
from whimdb.tasks import TaskBase


class ExpiredItemsCleanupTask(TaskBase):
    async def run(self):
        while True:
            self._logger.info("run")

            await asyncio.sleep(2)
