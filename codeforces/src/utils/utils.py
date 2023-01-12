from datetime import datetime

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


def to_date_str(timestamp: str) -> str:
    timestamp = to_int(timestamp)
    return datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y") if timestamp else DEFAULTS['str']


def isfloat(string: str) -> bool:
    try:
        float(string)
    except:
        return False

    return True

