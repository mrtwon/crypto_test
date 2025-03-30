from fastapi import APIRouter, Depends

from src.app.exception.tron import TronAddressNotFound
from src.app.routes.v1.tron.schema import TronBalanceSchema, SearchTronSchema
from src.infrastructure.database.statistics.interface import IStatisticsRepo
from src.infrastructure.database.statistics.model import StatisticsModel
from src.infrastructure.tron.interface import ITronRepo

tron_router = APIRouter(prefix='/tron')


@tron_router.post('/balance', response_model=TronBalanceSchema)
async def get_balance_router(
        schema: SearchTronSchema,
        tron_repo: ITronRepo = Depends(),
        statistics_repo: IStatisticsRepo = Depends()
):
    try:
        await statistics_repo.add(StatisticsModel(
            address=schema.address
        ))
        await statistics_repo.commit()
        result = tron_repo.get_balance_by_tron_address(schema.address)
        return TronBalanceSchema.model_validate({'balance': result})
    except Exception as e:
        raise TronAddressNotFound()
