import pytest

import settings
from codeforces.src.codeforces_api.api import CodeForcesApi
from codeforces.src.database.data_base import DbClient


@pytest.fixture
def codeforces_client():
    return CodeForcesApi()


def test_get_method(codeforces_client):

    urls = ["user.rating?handle=Pavelx4y16",
            "user.info?handles=Pavelx4y16"]
    data = [codeforces_client._get(url) for url in urls]

    assert len(data) == 2


def test_get_contests(codeforces_client):
    data = codeforces_client.get_contests("Pavelx4y16")

    assert len(data['result']) == 5


def test_get_user_info(codeforces_client):
    data = codeforces_client.get_user_info("Pavelx4y16")

    user_info = data['result'][0]
    assert user_info['rank'] == "specialist"
    assert user_info['rating'] >= 1000


def test_get_users_info(codeforces_client):
    students = DbClient(url=settings.cities_path).students
    users_info = list(codeforces_client.get_users_info(students))

    total = len(students)
    assert len(users_info) == total

    failed = len([user_info for user_info in users_info if user_info is None])
    print(f"Failure percentage: {failed / total}")  # failures may be here because of non-existing nick_names
