from fastapi import FastAPI, Depends

from src.app.di.di_setup import Session
from src.infrastructure.database.statistics.interface import IStatisticsRepo
from src.infrastructure.database.statistics.repo import StatisticsRepo


def get_stat(session: Session = Depends()):
    return StatisticsRepo(session)


def di_stat(app: FastAPI):
    app.dependency_overrides[IStatisticsRepo] = get_stat
