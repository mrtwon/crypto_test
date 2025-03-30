import datetime
import uuid
from uuid import UUID

from attrs import field

from src.infrastructure.database.base import entity


@entity
class StatisticsModel:
    id: UUID = field(factory=uuid.uuid4)
    address: str
    create_at: datetime.datetime = field(factory=datetime.datetime.now)