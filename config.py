from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_TRADING = BASE_DIR / "db" / "databases" / "trading.db"
DB_TESTING_STRATEGIES = BASE_DIR / "db" / "databases" / "test_strat.db"

START_DATE_COLLECTION_HISTORICAL_DATA = 1577829600  # 2020.01.01

AVAILABLE_MODES = [
    "trading",
    "test"
]

AVAILABLE_SYMBOLS = [
    "BTCUSDT",
    "ETHBTC"
]

AVAILABLE_TIMEFRAMES = [
    "1h"
]

CANDLE_MULTIPLIER = 2
