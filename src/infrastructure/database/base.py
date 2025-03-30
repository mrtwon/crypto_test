from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base
from attr import define

Base = declarative_base()

entity = define(slots=False, kw_only=True)


class ISQLAlchemyRepo:
    async def commit(self):
        ...

    async def rollback(self):
        ...


class SQLAlchemyRepo(ISQLAlchemyRepo):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
