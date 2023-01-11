import asyncio
import time
from typing import List

import aiohttp
import requests

from codeforces.src.database.data_classes import Student
from codeforces.src.utils.aiohttp_utils import with_session


class AsyncCodeForcesApi:
    def __init__(self, base_url="https://codeforces.com/api"):
        self.base_url = base_url

    async def _get(self, session: aiohttp.ClientSession, url: str) -> dict:
        async with session.get(f"{self.base_url}/{url}") as response:
            if response.status == 200:
                return await response.json()

    @with_session
    async def get_contests(self, nick_name: str, *, session: aiohttp.ClientSession = None):
        return await self._get(session, f"user.rating?handle={nick_name}")

    @with_session
    async def get_user_info(self, nick_name: str, *, session: aiohttp.ClientSession = None):
        return await self._get(session, f"user.info?handles={nick_name}")

    @with_session
    async def get_users_info(self, students: List[Student], *, session: aiohttp.ClientSession = None):
        coroutines = [self.get_user_info(student.nick_name, session=session) for student in students]
        return await asyncio.gather(*coroutines)


class CodeForcesApi:
    def __init__(self, base_url="https://codeforces.com/api"):
        self.base_url = base_url

    def _get(self, url: str) -> dict:
        time.sleep(2)
        response = requests.get(f"{self.base_url}/{url}")
        if response.status_code == 200:
            return response.json()

    def get_contests(self, nick_name: str):
        return self._get(f"user.rating?handle={nick_name}")

    def get_user_info(self, nick_name: str):
        return self._get(f"user.info?handles={nick_name}")

    def get_users_info(self, students: List[Student]):
        return (self.get_user_info(student.nick_name) for student in students)


