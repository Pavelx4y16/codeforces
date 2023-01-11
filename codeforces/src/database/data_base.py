import csv
from copy import deepcopy
from pathlib import Path
from typing import Dict, List

import requests
import six.moves.urllib.request as urlreq

import settings
from codeforces.src.database.data_classes import Student, StudentFields
from codeforces.src.database.serializer import Serializer
from codeforces.src.utils.singleton import Singleton
from codeforces.src.utils.utils import validate_arguments


@validate_arguments
class DbClient(Singleton):
    def __validate_init_arguments(self, url):
        assert isinstance(url, Path)
        assert url.is_dir()

    def __init__(self, url: Path):
        self.url = url
        self.cities = self._load_cities()

    def __enter__(self):
        self.cities = self._load_cities()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # self._update_db()
        pass

    @property
    def city_names(self):
        return self.cities.keys()

    @property
    def students(self) -> List[Student]:
        """Get all students for all cities"""
        all_students = []
        for students in self.cities.values():
            all_students += students

        return all_students

    def _update_db(self):
        HEADERS = list(deepcopy(Student.HEADERS))
        del HEADERS[StudentFields.CITY_NAME]

        for city_name, students in self.cities.items():
            with open(self.url / (city_name + ".csv"), mode='w', encoding="utf-8", newline='') as f:
                csv.writer(f).writerows([HEADERS] + students)

    def _load_cities(self, ignore_headers=True) -> Dict[str, List[Student]]:
        cities = dict()
        for file in self.url.iterdir():
            with open(file, mode='r', encoding="utf-8", newline='') as f:
                reader = csv.reader(f)
                if ignore_headers:
                    next(reader)
                students_info = (row[:1] + [file.stem.capitalize()] + row[1:] for row in reader)
                cities[file.stem] = Serializer.deserialize(students_info)
        return cities

    def _save_city(self, city_name, students: List[Student]):
        self.cities[city_name] = students
        self._update_db()

    def remove_student(self, city_name, nick_name):
        students = [student for student in self.cities[city_name] if student.nick_name != nick_name]
        self._save_city(city_name, students)

    def update_table(self):
        for city_name, students in self.cities.items():
            for student in students:
                # req = "https://codeforces.com/api/user.rating?handle=" + student.nick_name
                # response = requests.get(req, timeout=60)
                # coroutines = []
                if response.status_code != 200:
                    continue
                response = response.json()
                response = response.get('result')
                response = response[-1] if response else None
                if response:
                    student.last_round = response["contestName"]
                    student.date = response["ratingUpdateTimeSeconds"]
                    student.rating = response["newRating"]
            self._save_city(city_name, students)

    def _update_grade(self, number):
        for city_name, students in self.cities.items():
            for student in students:
                if student.grade:
                    student.grade += number
            self._save_city(city_name, students)

    def to_next_grade(self):
        self._update_grade(1)

    def to_prev_grade(self):
        self._update_grade(-1)

    def remove_graduated_students(self):
        for city_name, students in self.cities.items():
            self._save_city(city_name, [student for student in students if student.grade <= 11])

    def add_student(self, city_name, nickname, fio, grade, school_name):
        if not nickname:
            return "Никнейм не был введен"
        webp = urlreq.urlopen("https://codeforces.com/profile/" + nickname + "?locale=ru").read().decode("utf-8")
        ptrn = '<div style="font-size: 0.8em; color: #777;">'
        text = ""
        if not fio:
            fio = ""
            for line in webp:
                text = text + line
                pos = text.find(ptrn) + len(ptrn)
            if pos != 43:
                while text[pos] != '<' and text[pos] != ',':
                    fio += text[pos]
                    pos = pos + 1

        response = requests.get('https://codeforces.com/api/user.info?handles=' + nickname, params={"lang": "ru"})
        response = response.json()['result'][0]

        student_info = [response.get('rating'), city_name.capitalize()]
        fio = fio.strip() if fio else None
        if fio:
            fio = fio.split(" ")
            student_info.append(fio[0])
            if len(fio) == 2:
                student_info.append(fio[1])
            else:
                student_info.append(None)
        else:
            student_info += [None, None]
        student_info += [nickname, grade, school_name, None, None]

        new_student = Serializer.deserialize_one(student_info)
        self._save_city(city_name, self.cities[city_name] + [new_student])

#
# if __name__ == '__main__':
#     db_client = DbClient(settings.cities_path)
#     for name in db_client.city_names:
#         print(name)
