from sqlalchemy import select, func

from src.infrastructure.database.base import SQLAlchemyRepo
from src.infrastructure.database.statistics.interface import IStatisticsRepo
from src.infrastructure.database.statistics.model import StatisticsModel
from src.infrastructure.database.statistics.table import StatisticsTable


class StatisticsRepo(IStatisticsRepo, SQLAlchemyRepo):
    async def add(self, model: StatisticsModel) -> StatisticsModel:
        new_model = StatisticsTable(id=model.id, address=model.address, create_at=model.create_at)
        self.session.add(new_model)
        return model

    async def get_all(self, offset: int = 0, limit: int = 10) -> list[StatisticsModel]:
        stmt = select(StatisticsTable).order_by(StatisticsTable.create_at.desc()).offset(offset).limit(limit)
        result = (await self.session.scalars(stmt)).all()
        return [
            StatisticsModel(id=one.id, address=one.address, create_at=one.create_at)
            for one in result
        ]

    async def get_all_count(self) -> int:
        stmt = select(func.count()).select_from(StatisticsTable)
        result = (await self.session.execute(stmt)).mappings().one()
        return result['count']
