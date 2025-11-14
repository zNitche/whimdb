from dataclasses import dataclass
from whimdb.dataclasses.database import DatabaseItem


@dataclass
class DatabaseQueryResponse:
    items: list[DatabaseItem]
    total_pages: int | None = None
    page_id: int | None = None
