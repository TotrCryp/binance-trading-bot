from db.service import get_db


def save(strategy):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO trading_strategy (symbol, updated_at, percentage_min_profit, market_indicator_to_buy, 
                                          market_indicator_to_sell, candle_multiplier)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (strategy.symbol, strategy.updated_at, strategy.percentage_min_profit,
              strategy.market_indicator_to_buy, strategy.market_indicator_to_sell, strategy.candle_multiplier))

        strategy_id = cursor.lastrowid

        for part in strategy.deposit_division_strategy:
            cursor.execute("""
                INSERT INTO deposit_part (strategy_id, stage, percentage_of_deposit, price_change)
                VALUES (?, ?, ?, ?)
            """, (strategy_id, part.stage, part.percentage_of_deposit, part.price_change))

        conn.commit()
        return strategy_id


def get(strategy_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM trading_strategy WHERE id = ?", (strategy_id,))
        strategy_row = cursor.fetchone()
        if not strategy_row:
            return None

        strategy_dict = dict(strategy_row)

        cursor.execute(
            "SELECT stage, percentage_of_deposit, price_change FROM deposit_part WHERE strategy_id = ?",
            (strategy_id,)
        )
        deposit_parts = [dict(row) for row in cursor.fetchall()]

        return strategy_dict, deposit_parts
