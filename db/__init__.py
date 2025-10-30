from db.service import get_db

with get_db() as conn:
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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trading_session (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL,
        start_base_amount REAL NOT NULL,
        start_quote_amount REAL NOT NULL,
        stage INTEGER NOT NULL,
        average_cost_acquired_assets REAL NOT NULL,
        last_action TEXT NOT NULL, 
        strategy_id INTEGER NOT NULL,
        FOREIGN KEY(strategy_id) REFERENCES trading_strategy(id)
    )
    """)

    conn.commit()
