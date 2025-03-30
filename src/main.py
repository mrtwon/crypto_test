import asyncio

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.di.di_setup import get_session, Session, get_session_maker
from src.app.middleware import add_application_exception_handler
from src.app.routes.root import root_router
from src.app.di.di_all import di_all
from src.infrastructure.database.statistics.interface import IStatisticsRepo
from src.infrastructure.database.statistics.repo import StatisticsRepo
from src.infrastructure.tron.interface import ITronRepo
from src.infrastructure.tron.repo import TronRepo
from src.rabbitmq.base import ConsumeManager

app = FastAPI()

app.include_router(root_router)
add_application_exception_handler(app)
di_all(app)


@app.on_event('startup')
async def startup():
    session_make = get_session_maker()
    stat_repo = StatisticsRepo
    tron_repo = TronRepo
    loop = asyncio.get_event_loop()
    ConsumeManager(loop, tron_repo=tron_repo, stat_repo=stat_repo, session_make=session_make).start_all()