from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.config import settings


class Session:
    ...


async def get_session() -> AsyncSession:
    async_engine = create_async_engine(
        url=settings.DATABASE_URL_asyncpg
    )

    session = async_sessionmaker(async_engine)
    async with session(expire_on_commit=False) as s:
        yield s


def get_session_maker() -> async_sessionmaker[AsyncSession]:
    async_engine = create_async_engine(
        url=settings.DATABASE_URL_asyncpg
    )

    session = async_sessionmaker(async_engine)
    return session
# async def get_session_next() -> AsyncSession:
#     return await(anext(get_session()))

def di_setup(app: FastAPI):
    app.dependency_overrides[Session] = get_session
