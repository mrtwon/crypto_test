import pytest
from sqlalchemy import Engine, create_engine
from starlette.testclient import TestClient

from src.config import settings
from src.infrastructure.database.base import Base
from src.main import app
from src.infrastructure.database.statistics.interface import IStatisticsRepo
from src.infrastructure.database.statistics.repo import StatisticsRepo


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app=app)


@pytest.fixture(scope='session')
def engine() -> Engine:
    return create_engine(url=settings.DATABASE_URL_psycopg)


@pytest.fixture(autouse=True, scope='session')
def create_drop_db(engine: Engine):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
