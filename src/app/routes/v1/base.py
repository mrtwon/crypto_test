from fastapi import APIRouter
from .tron.route import tron_router
from .stat.route import stat_router

router_v1 = APIRouter(prefix='/v1')
router_v1.include_router(tron_router)
router_v1.include_router(stat_router)