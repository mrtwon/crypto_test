import datetime
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.base import Base


class StatisticsTable(Base):
    __tablename__ = 'statistics'
    id: Mapped[UUID] = mapped_column(primary_key=True, unique=True)
    address: Mapped[str] = mapped_column(nullable=False)
    create_at: Mapped[datetime.datetime] = mapped_column(nullable=False)

