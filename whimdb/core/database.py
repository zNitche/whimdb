from typing import Any
import copy
import re
import math
import time
from whimdb.dataclasses.database import DatabaseItem, DatabaseQueryResponse


class Database:
    def __init__(self):
        self.__content: dict[str, DatabaseItem] = {}

    @property
    def content(self):
        return copy.deepcopy(self.__content)

    def set(self, key: str, value: Any, ttl: int | None = None):
        created_at = time.time()

        self.__content[key] = DatabaseItem(
            value=value, created_at=created_at, ttl=ttl)
        
    def remove(self, key: str):
        if key in self.__content.keys():
            del self.__content[key]

    def purge(self):
        self.__content.clear()

    def query(self, key: str | None = None,
              regex_string: str | None = None,
              page_id: int = 0,
              items_per_page: int = 20) -> DatabaseQueryResponse | None:

        if not key and not regex_string:
            raise Exception("both key and search_regex can't be empty")

        if key and not regex_string:
            db_item = self.__content.get(key)

            if not db_item:
                return None

            return DatabaseQueryResponse(items=[db_item])

        regex = re.compile(fr"{regex_string}")

        results = [self.__content[key]
                   for key in self.__content.keys() if regex.search(key)]

        total_pages, paginated_results = self.__paginate_items(
            items=results, page_id=page_id, items_per_page=items_per_page)

        return DatabaseQueryResponse(items=paginated_results, total_pages=total_pages,
                                     page_id=page_id)

    def __paginate_items(self, items: list[DatabaseItem], page_id: int, items_per_page: int):
        total_keys = len(self.__content.keys())
        total_pages = math.ceil(
            total_keys / items_per_page) if total_keys > 0 else 1

        if page_id > total_pages:
            return total_pages, []

        offset = page_id * items_per_page
        limit = offset + items_per_page

        return total_pages, items[offset:limit]
