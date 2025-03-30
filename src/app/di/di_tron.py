from fastapi import FastAPI

from src.infrastructure.tron.interface import ITronRepo
from src.infrastructure.tron.repo import TronRepo


def get_tron():
    print('get tron')
    return TronRepo()


def di_tron(app: FastAPI):
    app.dependency_overrides[ITronRepo] = get_tron
