from abc import ABC

from src.infrastructure.database.base import ISQLAlchemyRepo
from src.infrastructure.database.statistics.model import StatisticsModel


class IStatisticsRepo(ABC, ISQLAlchemyRepo):
    async def add(self, model: StatisticsModel) -> StatisticsModel:
        ...

    async def get_all(self, offset: int = 0, limit: int = 10) -> list[StatisticsModel]:
        ...

    async def get_all_count(self) -> int:
        ...

    async def get_by_tron_address(self, tron_address: str) -> StatisticsModel | None:
        ...