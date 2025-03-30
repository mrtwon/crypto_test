from fastapi import APIRouter
from .v1.base import router_v1

root_router = APIRouter(prefix='/api')
root_router.include_router(router_v1)
