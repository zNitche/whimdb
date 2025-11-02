import logging


class Logger:
    def __init__(self, logger_name: str | None = None):

        self.enabled = True
        self.debug_mode = False

        self.backup_log_files_count = None
        self.logs_path = None

        self.__logger = logging.getLogger(
            __name__ if logger_name is None else logger_name)

    def init(self,
             debug: bool = False,
             enabled: bool = True):

        self.enabled = enabled
        self.debug_mode = debug

        if enabled:
            self.__setup()

    def __setup(self):
        self.__logger.setLevel("DEBUG" if self.debug_mode else "INFO")
        self.__setup_serial()

    def __setup_serial(self):
        formatter = self.__get_formatter(with_day=False)

        console_logger = logging.StreamHandler()
        console_logger.setFormatter(formatter)

        self.__logger.addHandler(console_logger)

    def __get_formatter(self, with_day: bool = True) -> logging.Formatter:
        format = "%Y-%m-%d %H:%M:%S" if with_day else "%H:%M:%S"

        formatter = logging.Formatter(
            "{asctime} - {name} - {levelname} - {message}",
            style="{",
            datefmt=format,
        )

        return formatter

    def exception(self, message: str):
        self.__logger.exception(message)

    def error(self, message: str):
        self.__logger.error(message)

    def info(self, message: str):
        self.__logger.info(message)

    def warning(self, message: str):
        self.__logger.warning(message)

    def debug(self, message: str):
        self.__logger.debug(message)
