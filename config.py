from pathlib import Path
import logging
from logging.handlers import TimedRotatingFileHandler

BASE_DIR = Path(__file__).resolve().parent
DB_TRADING = BASE_DIR / "db" / "databases" / "trading.db"
DB_TESTING_STRATEGIES = BASE_DIR / "db" / "databases" / "test_strat.db"

START_DATE_COLLECTION_HISTORICAL_DATA = 1577829600  # 2020.01.01


def setup_logging():
    # Console logging configuration
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # File logging configuration
    file_handler = TimedRotatingFileHandler('app.log', when='D', interval=1, backupCount=2)
    file_handler.setLevel(logging.INFO)

    # Log format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Handlers
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
