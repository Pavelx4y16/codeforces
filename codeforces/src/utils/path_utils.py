import pathlib


def recreate_file(file: pathlib.Path):
    with file.open(mode="w"):
        pass
