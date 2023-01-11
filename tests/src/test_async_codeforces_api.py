import asyncio

import aiohttp
import pytest

import settings
from codeforces.src.codeforces_api.api import AsyncCodeForcesApi
from codeforces.src.database.data_base import DbClient


@pytest.fixture
def async_codeforces_client():
    return AsyncCodeForcesApi()


async def test_get_method(async_codeforces_client):

    urls = ["user.rating?handle=Pavelx4y16",
            "user.info?handles=Pavelx4y16"]
    async with aiohttp.ClientSession() as session:
        coroutins = [async_codeforces_client._get(session, url) for url in urls]
        data = await asyncio.gather(*coroutins)

    assert len(data) == 2


async def test_get_contests(async_codeforces_client):
    coroutins = [async_codeforces_client.get_user_contests("Pavelx4y16")]
    data = await asyncio.gather(*coroutins)

    assert len(data[0]['result']) == 5


async def test_get_user_info(async_codeforces_client):
    coroutins = [async_codeforces_client.get_user_info("Pavelx4y16")]
    data = await asyncio.gather(*coroutins)

    user_info = data[0]['result'][0]
    assert user_info['rank'] == "specialist"
    assert user_info['rating'] >= 1000


async def test_get_users_info(async_codeforces_client):
    students = DbClient(url=settings.cities_path).students
    coroutins = [async_codeforces_client.get_users_info(students)]
    data = await asyncio.gather(*coroutins)

    users_info = data[0]
    total = len(students)
    assert len(users_info) == total

    failed = len([user_info for user_info in users_info if user_info is None])
    print(f"Failure procentage: {failed / total}")
