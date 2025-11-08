from typing import Any


class Database:
    def __init__(self):
        self.__content = {}

    def set(self, key: str, value: Any):
        self.__content[key] = value

    def query(self, key: str, regex_string: str | None = None):
        return self.__content.get(key)
