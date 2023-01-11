import pytest

import settings
from codeforces.src.codeforces_api.api import CodeForcesApi
from codeforces.src.database.data_base import DbClient


@pytest.fixture(scope="session")
def codeforces_client():
    return CodeForcesApi()


@pytest.fixture(scope="session")
def db_client():
    return DbClient(url=settings.cities_path)
