from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_TRADING = BASE_DIR / "db" / "databases" / "trading.db"
DB_TESTING_STRATEGIES = BASE_DIR / "db" / "databases" / "test_strat.db"
