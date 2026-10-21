from whimdb.dataclasses.database import DatabaseItem
from whimdb.dataclasses.communication import QueryItem


def db_items_to_query(items: list[DatabaseItem], keys_only: bool | None = False) -> list[QueryItem]:
    def to_none(item: DatabaseItem) -> DatabaseItem:
        item.value = None
        return item
    
    current_items = items

    if keys_only:
        current_items = [to_none(item) for item in items]

    return [QueryItem.from_dict(**item.__dict__)
            for item in current_items]
