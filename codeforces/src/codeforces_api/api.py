import asyncio
import time
from typing import List

import aiohttp
import requests

from codeforces.src.database.data_classes import Student
from codeforces.src.utils.aiohttp_utils import with_session
from codeforces.src.utils.codeforces_utils import ParsedResponse
from codeforces.src.utils.logger import Logger
from codeforces.src.utils.observer import ObserverSubject
from codeforces.src.utils.utils import Delays

logger = Logger(__name__)


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


class CodeForcesApi(ObserverSubject):
    def __init__(self, home_url="https://codeforces.com/", lang="ru"):
        super().__init__()

        self.home_url = home_url
        self.base_params = {'lang': lang}

    def _get(self, url: str) -> ParsedResponse:
        time.sleep(Delays.CODE_FORCES.value)
        response = requests.get(f"{self.home_url}{url}", params=self.base_params)

        return ParsedResponse(response)

    def get_user_profile(self, nick_name):
        response = self._get(f"profile/{nick_name}")
        if response.status_code == 200:
            return response

    def update_nick_name(self, nick_name: str) -> str:
        response = self.get_user_profile(nick_name)
        if response.status_code == 200 and response.url != self.home_url:
            nick_name = response.url.split('/')[-1]

            # it can happen that url has some parameters, like:
            # http/.../nick_name?lang=ru...
            # so, we need to exclude those parameters from nick_name
            position_of_parameters_sign = nick_name.find("?")
            if position_of_parameters_sign != -1:
                nick_name = nick_name[:position_of_parameters_sign]

            return nick_name

    def get_user_contests(self, student: Student) -> dict:
        response = self._get(f"api/user.rating?handle={student.nick_name}")
        if response.status_code != 200 and \
                f"handle: User {student.nick_name} not found" in response.reason:
            updated_nick_name = self.update_nick_name(student.nick_name)

            if updated_nick_name:
                response = self._get(f"api/user.rating?handle={updated_nick_name}")
                student.nick_name = updated_nick_name  # save
        if response.status_code == 200:
            return response.result

    def get_users_contests(self, students: List[Student]) -> dict:
        users_contests = dict()
        for processed, student in enumerate(students, start=1):
            # todo: vanish variable 'user_contests'
            user_contests = self.get_user_contests(student)
            self.notify(processed / len(students))
            users_contests[student.nick_name] = user_contests

        return users_contests

    def get_user_info(self, nick_names: str) -> dict:
        users_info = self._get(f"api/user.info?handles={nick_names}")
        if users_info.status_code == 200:
            return users_info.result[0]

    def get_users_info(self, students: List[Student]) -> dict:
        # todo: this works only if all nick_names are valid
        #       return self.get_user_info(';'.join([student.nick_name for student in students]))
        # consider nick validation (maybe filter out all nicks as the application starts)
        return {student.nick_name: self.get_user_info(student.nick_name) for student in students}

