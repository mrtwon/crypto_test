import datetime
from uuid import UUID

from pydantic import BaseModel


class StatisticSchema(BaseModel):
    id: UUID
    address: str
    create_at: datetime.datetime


class PaginationStatisticSchema(BaseModel):
    statistics: list[StatisticSchema]
    current_page: int
    next_page: int | None = None
    all_pages: int
