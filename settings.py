import os
from pathlib import Path

cities_path = Path(os.environ.get('DataBaseURL')) if os.environ.get('DataBaseURL') else Path("codeforces/resources") / "cities"
logger_path = Path("./logs")
