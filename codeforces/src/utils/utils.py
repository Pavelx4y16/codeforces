from enum import Enum, auto
from datetime import datetime
from typing import Union

DEFAULTS = {'int': 0, 'str': "UNKNOWN"}


def validate_arguments(cls):
    orig_init = cls.__init__

    def dec_init(self, *args, **kwargs):
        validate = getattr(self, f"_{cls.__name__}__validate_init_arguments")
        validate(*args, **kwargs)
        orig_init(self, *args, **kwargs)

    cls.__init__ = dec_init

    return cls


def to_int(string: str) -> int:
    return int(float(string)) if isfloat(string) else DEFAULTS['int']


def to_str(value: Union[str, int]) -> str:
    return str(value).strip() or DEFAULTS['str']


def to_date_str(timestamp: str) -> str:
    timestamp = to_int(timestamp)
    return datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y") if timestamp else DEFAULTS['str']


def isfloat(string: str) -> bool:
    try:
        float(string)
    except:
        return False

    return True


class Delays(Enum):
    CODE_FORCES = 2


class AppOptionality(Enum):
    SHOW_TABS = 0
    SORT_STUDENTS = auto()
    CHANGE_LAST_ROUND_VIEW = auto()
    CHANGE_SCHOOL_VIEW = auto()
    ADD_STUDENT = auto()
    REMOVE_STUDENT = auto()
    REMOVE_GRADUATED_STUDENTS = auto()
    UPDATE_CONTESTS = auto()
    GRADE_STUDENTS_UP = auto()
    GRADE_STUDENTS_DOWN = auto()
    SHOW_STUDENTS_TABLE = auto()
