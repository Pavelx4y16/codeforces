import pathlib
from datetime import datetime

import settings
from codeforces.src.utils.utils import validate_arguments


@validate_arguments
class Logger:
    def __validate_init_arguments(self, name, path=settings.logger_path):
        assert isinstance(name, str)
        assert isinstance(path, pathlib.Path)
        assert path.is_dir()

    def __init__(self, name, path=settings.logger_path):
        path.mkdir(exist_ok=True)
        self.logger_file = path / f"{name}_{datetime.now()}.log"

    def log(self, message: str):
        with self.logger_file.open(mode="a") as file:
            file.write(f"{message}\n")
