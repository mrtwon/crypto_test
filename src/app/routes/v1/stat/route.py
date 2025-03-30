from fastapi import APIRouter, Depends
import math
from src.app.routes.v1.stat.schema import StatisticSchema, PaginationStatisticSchema
from src.infrastructure.database.statistics.interface import IStatisticsRepo

stat_router = APIRouter()


@stat_router.get('/statistics', response_model=PaginationStatisticSchema)
async def get_statistics_router(
        page: int = 1,
        statistic_repo: IStatisticsRepo = Depends()
):
    current_page = page
    offset_const = 10
    limit = 10

    get_all_count = await statistic_repo.get_all_count()
    all_pages = math.ceil(get_all_count/offset_const)
    current_offset = offset_const * (current_page-1)
    result_get_all_statistics = await statistic_repo.get_all(offset=current_offset, limit=limit)

    return PaginationStatisticSchema.model_validate({
        'statistics': [StatisticSchema.model_validate(one.__dict__) for one in result_get_all_statistics],
        'current_page': current_page,
        'next_page': None if current_page >= all_pages else current_page+1,
        'all_pages': all_pages
    })