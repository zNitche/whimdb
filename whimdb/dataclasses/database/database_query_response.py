from dataclasses import dataclass
from whimdb.dataclasses.database import DatabaseItem


@dataclass
class DatabaseQueryResponse:
    items: list[DatabaseItem]
    total_pages: int = 1
    page_id: int = 0
