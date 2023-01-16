import csv
from copy import deepcopy
from pathlib import Path
from typing import Dict, List

from codeforces.src.database.data_classes import Student, StudentFields
from codeforces.src.database.serializer import Serializer
from codeforces.src.utils.singleton import Singleton
from codeforces.src.utils.str_utils import split_fio
from codeforces.src.utils.utils import validate_arguments


@validate_arguments
class DbClient(Singleton):
    def __validate_init_arguments(self, url):
        assert isinstance(url, Path)
        assert url.is_dir()

    def __init__(self, url: Path):
        self.url = url
        self.cities = self._load_cities()

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

    def update_users_contests(self, users_contests_info, students: List[Student]):
        for student in students:
            user_contests_info = users_contests_info[student.nick_name]
            if user_contests_info:
                last_contest = user_contests_info[-1]
                student.last_round = last_contest["contestName"]
                student.date = last_contest["ratingUpdateTimeSeconds"]
                student.rating = last_contest["newRating"]
        self._update_db()

    def _update_grade(self, number):
        for city_name, students in self.cities.items():
            for student in students:
                if student.grade:
                    student.grade += number
            self._save_city(city_name, students)  # Student's objects are references here --- not necessary to save them

    def to_next_grade(self):
        self._update_grade(1)

    def to_prev_grade(self):
        self._update_grade(-1)

    def _filter_out_graduated_students(self, students: List[Student]) -> List[Student]:
        return [student for student in students if student.grade <= 11]

    def remove_graduated_students(self, city_name=None):
        if city_name:
            return self._save_city(city_name, self._filter_out_graduated_students(self.cities[city_name]))

        for city_name, students in self.cities.items():
            self._save_city(city_name, self._filter_out_graduated_students(students))

    def add_student(self, city_name, nick_name, fio, grade, school_name, user_info):
        if not nick_name:
            raise Exception("fill 'nick_name' field")
        if not user_info:
            raise Exception(f"there is no user with such nick_name: {nick_name}")

        student_info = [user_info.get('rating'), user_info.get('city') or city_name.capitalize()]

        last_name, first_name = split_fio(fio)
        student_info += [last_name or user_info.get('lastName'), first_name or user_info.get('firstName'),
                         nick_name, grade, school_name or user_info.get('organization'), None, None]

        new_student = Serializer.deserialize_one(student_info)
        self._save_city(city_name, self.cities[city_name] + [new_student])

#
# if __name__ == '__main__':
#     db_client = DbClient(settings.cities_path)
#     for name in db_client.city_names:
#         print(name)
