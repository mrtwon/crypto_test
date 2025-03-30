import asyncio
from typing import Callable, Awaitable

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .consume_tron import ConsumeTron
from .consumer_statistics import ConsumeStatistics
from ..infrastructure.database.statistics.interface import IStatisticsRepo
from ..infrastructure.database.statistics.repo import StatisticsRepo
from ..infrastructure.tron.interface import ITronRepo
from ..infrastructure.tron.repo import TronRepo


class ConsumeManager:
    def __init__(
            self,
            loop,
            tron_repo: type[ITronRepo],
            stat_repo: type[IStatisticsRepo],
            session_make: Awaitable[Callable[[], async_sessionmaker[AsyncSession]]],
    ):
        self.loop = loop
        self.tron_repo = tron_repo
        self.stat_repo = stat_repo
        self.session_make = session_make

    def start_all(self):
        consumer_tron = ConsumeTron(
            loop=self.loop,
            tron_repo=self.tron_repo,
            stat_repo=self.stat_repo,
            session_make=self.session_make
        )
        asyncio.ensure_future(consumer_tron.start_consume())

        consumer_stat = ConsumeStatistics(
            loop=self.loop,
            stat_repo=self.stat_repo,
            session_make=self.session_make
        )
        asyncio.ensure_future(consumer_stat.start_consume())
