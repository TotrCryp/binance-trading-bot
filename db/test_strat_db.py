class CandlesDAO:
    def __init__(self, conn, candle_table_name):
        self._conn = conn
        self._candle_table_name = candle_table_name

        self._conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {self._candle_table_name} (
                open_time INTEGER,
                open_price REAL,
                high_price REAL,
                low_price REAL,
                close_price REAL,
                volume REAL,
                close_time INTEGER,
                quote_asset_volume REAL,
                number_of_trades INTEGER,
                taker_buy_base_asset_volume REAL,
                taker_buy_quote_asset_volume REAL,
                unused_field TEXT
            );
        """)

    def get_candles(self):
        cur = self._conn.cursor()
        cur.execute(f"SELECT * FROM {self._candle_table_name}")
        return cur.fetchall()

    def set_candles(self, dataset):
        cur = self._conn.cursor()
        cur.executemany(f"""INSERT INTO {self._candle_table_name} (open_time, 
                        open_price,
                        high_price,
                        low_price,
                        close_price,
                        volume,
                        close_time,
                        quote_asset_volume,
                        number_of_trades,
                        taker_buy_base_asset_volume,
                        taker_buy_quote_asset_volume,
                        unused_field) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""", dataset)
        self._conn.commit()

    def get_last_timestamp(self):
        cur = self._conn.cursor()
        cur.execute(f"SELECT close_time FROM {self._candle_table_name} ORDER BY close_time DESC LIMIT 1")
        return cur.fetchone()


class TestResultsDAO:
    def __init__(self, conn):
        self._conn = conn

        self._conn.execute(f"""
            CREATE TABLE IF NOT EXISTS tests_results (
                symbol TEXT,
                start_time INTEGER,
                start_base_amount REAL,
                start_quote_amount REAL,
                number_transactions INTEGER,
                last_transactions_side TEXT,
                finish_time INTEGER,
                finish_base_amount REAL,
                finish_quote_amount REAL,
                percentage_of_profit REAL,
                deposit_division_strategy TEXT,
                percentage_strategy TEXT,
                market_indicators_strategy TEXT
            );
        """)

    def get_tests_results(self):
        cur = self._conn.cursor()
        cur.execute(f"SELECT * FROM tests_results")
        return cur.fetchone()
