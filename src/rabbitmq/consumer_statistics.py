import json
import math
from typing import Callable, Awaitable

import aio_pika
from aio_pika import Message
from aio_pika.abc import AbstractChannel, AbstractIncomingMessage
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from tronpy.exceptions import BadAddress

from src.app.routes.v1.stat.schema import StatisticSchema, PaginationStatisticSchema
from src.infrastructure.database.statistics.interface import IStatisticsRepo
from src.infrastructure.database.statistics.model import StatisticsModel
from src.infrastructure.tron.interface import ITronRepo


class ConsumeStatistics:
    def __init__(
            self,
            loop,
            session_make: [Callable[[], async_sessionmaker[AsyncSession]]],
            stat_repo: type[IStatisticsRepo]
    ):
        self.queue_name = 'get_statistics'
        self.loop = loop
        self.stat_repo = stat_repo
        self.session_make = session_make

    async def process_callback(
            self,
            session: AsyncSession,
            data: str,
            message: AbstractIncomingMessage,
            channel: AbstractChannel
    ):
        create_stat_repo = self.stat_repo(session)

        current_page = json.loads(data)['page']
        offset_const = 10
        limit = 10

        get_all_count = await create_stat_repo.get_all_count()
        all_pages = math.ceil(get_all_count / offset_const)
        current_offset = offset_const * (current_page - 1)
        result_get_all_statistics = await create_stat_repo.get_all(offset=current_offset, limit=limit)

        result = PaginationStatisticSchema.model_validate({
            'statistics': [StatisticSchema.model_validate(one.__dict__) for one in result_get_all_statistics],
            'current_page': current_page,
            'next_page': None if current_page >= all_pages else current_page + 1,
            'all_pages': all_pages
        })
        result_json = result.model_dump_json()

        await channel.default_exchange.publish(
            Message(
                bytes(json.dumps(result_json), 'utf-8'),
                content_type='application/json'
            ), routing_key=message.reply_to
        )

    async def pre_process(
            self,
            data: str,
            message: AbstractIncomingMessage,
            channel: AbstractChannel):
        async with self.session_make() as session:
            await self.process_callback(
                session=session,
                data=data,
                message=message,
                channel=channel
            )

    async def start_consume(self):
        connection = await aio_pika.connect_robust("amqp://guest:guest@192.168.0.19/", loop=self.loop)
        channel: aio_pika.abc.AbstractChannel = await connection.channel()
        queue: aio_pika.abc.AbstractQueue = await channel.declare_queue(
            self.queue_name
        )
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    await self.pre_process(
                        data=message.body.decode(),
                        message=message,
                        channel=channel
                    )
                    if queue.name in message.body.decode():
                        break
