from fastapi import FastAPI, HTTPException
from starlette.requests import Request

from src.app.exception.base import AppBaseException


def add_application_exception_handler(app: FastAPI):
    @app.exception_handler(AppBaseException)
    async def handler(request: Request, exc: AppBaseException):
        raise HTTPException(detail=exc.details, status_code=exc.status)
