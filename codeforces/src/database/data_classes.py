from enum import unique, IntEnum, auto, Enum

from dash import html

from codeforces.src.utils.utils import validate_arguments, to_date_str, DEFAULTS


@unique
class SortFields(Enum):
    RATING = "rating"
    FIO = "fio"
    GRADE = "grade"
    DATE = "date"
    ROUNDS_NUMBER = "rounds_number"


@unique
class StudentFields(IntEnum):
    RATING = 0
    CITY_NAME = auto()
    LAST_NAME = auto()
    FIRST_NAME = auto()
    NICK_NAME = auto()
    GRADE = auto()
    SCHOOL_NAME = auto()
    LAST_ROUND = auto()
    DATE = auto()
    ROUNDS_NUMBER = auto()


@validate_arguments
class Student:
    _rating_color_scale = {3000: "black", 2400: "red", 2100: "orange", 1900: "purple",
                           1600: "blue", 1400: "cyan", 1200: "green", 0: "grey"}
    sort_map = {SortFields.RATING: lambda student: student.rating,
                SortFields.FIO: lambda student: student.last_name + student.first_name,
                SortFields.GRADE: lambda student: student.grade,
                SortFields.DATE: lambda student: student.date if student.date != DEFAULTS['str'] else "0" * 10,
                SortFields.ROUNDS_NUMBER: lambda student: student.rounds_number}
    HEADERS = ("Рейтинг", "Город", "Фамилия", "Имя", "Никнейм", "Класс", "Учебное заведение", "Последний раунд", "Дата",
               "Количество раундов")
    view_school_attributes = True  # make 'grade' and 'school_name' attributes visible
    view_last_round_attributes = True  # make 'last_round' name visible
    view_city_name = False

    def __validate_init_arguments(self, rating, city_name, last_name, first_name, nick_name, grade, school_name,
                                  last_round, date, rounds_number):
        def _validate_arguments_on_type(arguments, type_):
            assert all([argument is not None and isinstance(argument, type_) for argument in arguments])

        _validate_arguments_on_type([rating, grade, rounds_number], int)
        _validate_arguments_on_type([city_name, last_name, first_name, nick_name, school_name, last_round, date], str)

    def __init__(self, rating: int, city_name: str, last_name: str, first_name: str, nick_name: str,
                 grade: int, school_name: str, last_round: str, date: str, rounds_number: int):
        self.rating = rating
        self._city_name = city_name
        self.last_name = last_name
        self.first_name = first_name
        self.nick_name = nick_name
        self.grade = grade
        self.school_name = school_name
        self.last_round = last_round
        self.date = date
        self.rounds_number = rounds_number

    @property
    def city_name(self):
        return self._city_name

    @property
    def color(self):
        for rating, color in self._rating_color_scale.items():
            if self.rating >= rating:
                return color

    def __iter__(self):
        return (self.__dict__[attr] for attr in self.__dict__ if not attr.startswith('_'))

    def display(self) -> dict:
        attributes = {StudentFields.RATING: self.rating}
        if self.view_city_name:
            attributes[StudentFields.CITY_NAME] = self.city_name
        attributes[StudentFields.LAST_NAME] = html.A(self.last_name, href='https://codeforces.com/profile/' + self.nick_name, style={'color': self.color})
        attributes[StudentFields.FIRST_NAME] = html.A(self.first_name, href='https://codeforces.com/profile/' + self.nick_name, style={'color': self.color})

        if self.view_school_attributes:
            attributes[StudentFields.GRADE] = self.grade
            attributes[StudentFields.SCHOOL_NAME] = self.school_name

        if self.view_last_round_attributes:
            attributes[StudentFields.LAST_ROUND] = self.last_round

        attributes[StudentFields.DATE] = to_date_str(self.date)
        attributes[StudentFields.ROUNDS_NUMBER] = self.rounds_number

        return attributes

    @staticmethod
    def display_headers():
        headers = [Student.HEADERS[StudentFields.RATING]]
        if Student.view_city_name:
            headers.append(Student.HEADERS[StudentFields.CITY_NAME])
        headers += [
            Student.HEADERS[StudentFields.LAST_NAME],
            Student.HEADERS[StudentFields.FIRST_NAME]
        ]
        if Student.view_school_attributes:
            headers += [Student.HEADERS[StudentFields.GRADE], Student.HEADERS[StudentFields.SCHOOL_NAME]]
        if Student.view_last_round_attributes:
            headers.append(Student.HEADERS[StudentFields.LAST_ROUND])
        headers += [Student.HEADERS[StudentFields.DATE], Student.HEADERS[StudentFields.ROUNDS_NUMBER]]

        return headers

    def __str__(self):
        return ','.join(str(attr) for attr in self.__dict__.values())


if __name__ == "__main__":
    for attr in Student():
        print(attr)
