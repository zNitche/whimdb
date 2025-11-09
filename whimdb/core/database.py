from typing import Any
import re


class Database:
    def __init__(self):
        self.__content = {}

    def set(self, key: str, value: Any):
        self.__content[key] = value

    def query(self, key: str | None = None, regex_string: str | None = None):
        if not key and not regex_string:
            raise Exception("both key and search_regex can't be empty")

        if key and not regex_string:
            return self.__content.get(key)

        regex = re.compile(fr"{regex_string}")

        results = [self.__content[key]
                   for key in self.__content.keys() if regex.search(key)]

        return results
