import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "app_data.sqlite3"

STRAT_FILE_PATH = BASE_DIR / "database" / "strategy.json"

SYMBOL = "BTCUSDT"  # get from ENV

BINANCE_API_KEY = os.getenv("SANDBOX_API_KEY")
BINANCE_API_SECRET = os.getenv("SANDBOX_API_SECRET")
# BINANCE_BASE_URL = "https://api.binance.com/api/v3"
BINANCE_BASE_URL = "https://testnet.binance.vision/api/v3"
