from whimdb import Logger


class TaskBase:
    def __init__(self):
        self._logger = Logger(self.__class__.__name__)

        self.__setup()

    def __setup(self):
        self._logger.init()

    async def run(self):
        raise NotImplementedError()
