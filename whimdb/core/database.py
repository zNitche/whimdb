from typing import Any
import re
import time
from whimdb.types import DatabaseItem


class Database:
    def __init__(self):
        self.__content: dict[str, DatabaseItem] = {}

    @property
    def content(self):
        return self.__content

    def set(self, key: str, value: Any, ttl: int | None = None):
        created_at = time.time()

        self.__content[key] = DatabaseItem(
            value=value, created_at=created_at, ttl=ttl)

    def query(self, key: str | None = None,
              regex_string: str | None = None) -> list[DatabaseItem] | None:

        if not key and not regex_string:
            raise Exception("both key and search_regex can't be empty")

        if key and not regex_string:
            db_item = self.__content.get(key)

            if not db_item:
                return None

            return [db_item]

        regex = re.compile(fr"{regex_string}")

        results = [self.__content[key]
                   for key in self.__content.keys() if regex.search(key)]

        return results
