import time


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


def to_str(string: str) -> str:
    string = string.strip() if isinstance(string, str) else None
    return string or DEFAULTS['str']


def to_date_str(date: str) -> str:
    date = to_int(date)
    return time.strftime("%d.%m.%Y", time.gmtime(date)) if date else DEFAULTS['str']


def isfloat(string: str) -> bool:
    try:
        float(string)
    except:
        return False

    return True
