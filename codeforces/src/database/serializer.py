from typing import List, Iterable

from codeforces.src.database.data_classes import Student, StudentFields
from codeforces.src.utils.utils import to_int, to_str


class Serializer:
    @staticmethod
    def serialize_one(obj: object) -> str:
        return str(obj)

    @staticmethod
    def serialize(objs: List[object]) -> List[str]:
        return [Serializer.serialize_one(obj) for obj in objs]

    @staticmethod
    def deserialize_one(student_info: List[str]) -> Student:
        student_info[StudentFields.RATING] = to_int(student_info[StudentFields.RATING])
        student_info[StudentFields.CITY_NAME] = to_str(student_info[StudentFields.CITY_NAME])
        student_info[StudentFields.LAST_NAME] = to_str(student_info[StudentFields.LAST_NAME])
        student_info[StudentFields.FIRST_NAME] = to_str(student_info[StudentFields.FIRST_NAME])
        student_info[StudentFields.NICK_NAME] = to_str(student_info[StudentFields.NICK_NAME])
        student_info[StudentFields.GRADE] = to_int(student_info[StudentFields.GRADE])
        student_info[StudentFields.SCHOOL_NAME] = to_str(student_info[StudentFields.SCHOOL_NAME])
        student_info[StudentFields.LAST_ROUND] = to_str(student_info[StudentFields.LAST_ROUND])
        student_info[StudentFields.DATE] = to_str(student_info[StudentFields.DATE])

        return Student(*tuple(student_info))

    @staticmethod
    def deserialize(students: Iterable[List[str]]) -> List[Student]:
        return [Serializer.deserialize_one(student) for student in students]


if __name__ == "__main__":
    s = ["1", "2", "3", "4", "5"]
    student = Serializer.deserialize_one(s)
    ss = Serializer.serialize_one(student)
    print(type(student), student)
    print(type(ss), ss)
