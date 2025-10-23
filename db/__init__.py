import sqlite3
from core.config import DB_PATH


conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS trading_strategy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    updated_at INTEGER NOT NULL,
    percentage_min_profit REAL NOT NULL,
    market_indicator_to_buy INTEGER NOT NULL,
    market_indicator_to_sell INTEGER NOT NULL,
    candle_multiplier INTEGER NOT NULL
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS deposit_part (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    strategy_id INTEGER NOT NULL,
    stage INTEGER NOT NULL,
    percentage_of_deposit INTEGER NOT NULL,
    price_change REAL NOT NULL,
    FOREIGN KEY(strategy_id) REFERENCES trading_strategy(id)
)
""")


conn.commit()
