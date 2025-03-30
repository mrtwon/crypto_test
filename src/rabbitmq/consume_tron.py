import json
from typing import Callable, Awaitable

import aio_pika
from aio_pika import Message
from aio_pika.abc import AbstractChannel, AbstractIncomingMessage
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from tronpy.exceptions import BadAddress

from src.infrastructure.database.statistics.interface import IStatisticsRepo
from src.infrastructure.database.statistics.model import StatisticsModel
from src.infrastructure.tron.interface import ITronRepo


class ConsumeTron:
    def __init__(
            self,
            loop,
            session_make: [Callable[[], async_sessionmaker[AsyncSession]]],
            tron_repo: type[ITronRepo],
            stat_repo: type[IStatisticsRepo]
    ):
        self.queue_name = 'get_balance'
        self.loop = loop
        self.tron_repo = tron_repo
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
        create_tron_repo = self.tron_repo()

        result_data: float | None = None
        result_status_code: int

        try:
            new_model = StatisticsModel(address=data)
            print(session.is_active)
            await create_stat_repo.add(new_model)
            await create_stat_repo.commit()
            print(session.is_active)
            result_data = float(create_tron_repo.get_balance_by_tron_address(data))
            result_status_code = 200
        except BadAddress:
            result_status_code = 404
        except Exception as e:
            print(e)
            result_status_code = 500

        result_json = {
            'status_code': result_status_code,
            'result': result_data
        }

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
