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
        return Student(to_int(student_info[StudentFields.RATING]),
                       to_str(student_info[StudentFields.CITY_NAME]),
                       to_str(student_info[StudentFields.LAST_NAME]),
                       to_str(student_info[StudentFields.FIRST_NAME]),
                       to_str(student_info[StudentFields.NICK_NAME]),
                       to_int(student_info[StudentFields.GRADE]),
                       to_str(student_info[StudentFields.SCHOOL_NAME]),
                       to_str(student_info[StudentFields.LAST_ROUND]),
                       to_str(student_info[StudentFields.DATE]),
                       to_int(student_info[StudentFields.ROUNDS_NUMBER]))

    @staticmethod
    def deserialize(students_info: Iterable[List[str]]) -> List[Student]:
        return [Serializer.deserialize_one(student_info) for student_info in students_info]


if __name__ == "__main__":
    s = [str(index) for index in range(1, 11)]
    student = Serializer.deserialize_one(s)
    ss = Serializer.serialize_one(student)
    print(type(student), student)
    print(type(ss), ss)
