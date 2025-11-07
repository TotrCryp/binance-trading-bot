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
        finish_base_amount REAL NOT NULL,
        finish_quote_amount REAL NOT NULL,
        stage INTEGER NOT NULL,
        average_cost_acquired_assets REAL NOT NULL,
        last_action TEXT NOT NULL, 
        strategy_id INTEGER NOT NULL,
        start_time INTEGER,
        FOREIGN KEY(strategy_id) REFERENCES trading_strategy(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        symbol TEXT NOT NULL,
        order_list_id INTEGER NOT NULL,
        client_order_id TEXT,
        transact_time INTEGER,
        price REAL,
        orig_qty REAL,
        executed_qty REAL,
        orig_quote_order_qty REAL,
        cummulative_quote_qty REAL,
        status TEXT,
        time_in_force TEXT,
        type TEXT,
        side TEXT,
        working_time INTEGER,
        session_id INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        price REAL,
        qty REAL,
        commission REAL,
        commission_asset TEXT,
        trade_id INTEGER,
        FOREIGN KEY(order_id) REFERENCES orders(order_id) ON DELETE CASCADE
    )
    """)

    conn.commit()
