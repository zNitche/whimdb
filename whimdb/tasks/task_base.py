from whimdb.core.utils import Logger


class TaskBase:
    def __init__(self, debug: bool = False):
        self._debug = debug

        self._logger = Logger(self.__class__.__name__)

        self.__setup()

    def __setup(self):
        self._logger.init(debug=self._debug)

    async def run(self):
        raise NotImplementedError()
