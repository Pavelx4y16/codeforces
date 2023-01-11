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
    async def get_user_contests(self, nick_name: str, *, session: aiohttp.ClientSession = None):
        return await self._get(session, f"user.rating?handle={nick_name}")

    @with_session
    async def get_user_info(self, nick_name: str, *, session: aiohttp.ClientSession = None):
        return await self._get(session, f"user.info?handles={nick_name}")

    @with_session
    async def get_users_info(self, students: List[Student], *, session: aiohttp.ClientSession = None):
        coroutines = [self.get_user_info(student.nick_name, session=session) for student in students]
        return await asyncio.gather(*coroutines)


class CodeForcesApi:
    def __init__(self, base_url="https://codeforces.com/api", lang="ru"):
        self.base_url = base_url
        self.base_params = {'lang': lang}

    def _get(self, url: str) -> list:
        time.sleep(2)
        response = requests.get(f"{self.base_url}/{url}", params=self.base_params)
        if response.status_code == 200:
            return response.json()['result']

    def get_user_contests(self, nick_name: str):
        return self._get(f"user.rating?handle={nick_name}")

    def get_users_contests(self, students: List[Student]) -> dict:
        return {student.nick_name: self.get_user_contests(student.nick_name) for student in students}

    def get_user_info(self, nick_names: str):
        users_info = self._get(f"user.info?handles={nick_names}")
        if users_info:
            return users_info[0]

    def get_users_info(self, students: List[Student]) -> dict:
        # todo: this works only if all nick_names are valid
        #       return self.get_user_info(';'.join([student.nick_name for student in students]))
        # consider nick validation (maybe filter out all nicks as the application starts)
        return {student.nick_name: self.get_user_info(student.nick_name) for student in students}

