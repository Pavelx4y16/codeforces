from abc import ABCMeta


class SingletonMeta(ABCMeta):
    """MetaClass. Should be used as metaclass property while class creating."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(cls.__class__, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):
    """This class created for convenience.
    To make some class Singleton this class can be used, but you also can use SingletonMeta instead."""
    pass
