class TradingLogDAO:
    def __init__(self, conn):
        self._conn = conn
        self._conn.execute(f"""
            CREATE TABLE IF NOT EXISTS orders (
                symbol TEXT,
                orderId INTEGER,
                clientOrderId TEXT,
                transactTime INTEGER,
                price REAL,
                origQty REAL,
                executedQty REAL,
                origQuoteOrderQty REAL,
                cummulativeQuoteQty REAL,
                status TEXT,
                timeInForce TEXT,
                type TEXT,
                side TEXT,
                workingTime INTEGER
            );
        """)

        self._conn.execute(f"""
            CREATE TABLE IF NOT EXISTS orders_fills (
                symbol TEXT,
                orderId INTEGER,
                clientOrderId TEXT,
                price REAL,
                qty REAL,
                commission REAL,
                commissionAsset TEXT,
                tradeId INTEGER
            );
        """)
