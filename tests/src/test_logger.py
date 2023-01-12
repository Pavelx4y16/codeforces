import settings
from codeforces.src.utils.logger import Logger


def test_logger():
    logger = Logger(__name__)
    logger.log("Test logging...")
    logger.log("Second Line")
    with (settings.logger_path / f"{__name__}.log").open(mode="r") as file:
        assert len(file.readlines()) == 2
