import os
from pathlib import Path

cities_path = os.environ.get('DataBaseURL') or Path("codeforces/resources") / "cities"
logger_path = Path("./logs")
