from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "app_data.sqlite3"
DB_URL = f"sqlite:///{DB_PATH}"
DB_ECHO = False

STRAT_FILE_PATH = BASE_DIR / "database" / "strategy.json"

SYMBOL = "BTCUSDT"  # get from ENV
