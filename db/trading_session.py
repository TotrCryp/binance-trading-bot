from db.service import get_db


def save(session):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO trading_session (symbol, start_base_amount, start_quote_amount, stage, 
                                          average_cost_acquired_assets, last_action, strategy_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (session.symbol, session.start_base_amount, session.start_quote_amount,
              session.stage, session.average_cost_acquired_assets, session.last_action, session.strategy_id))

        session_id = cursor.lastrowid
        conn.commit()
        return session_id


def get(session_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM trading_session WHERE id = ?", (session_id,))
        session_row = cursor.fetchone()
        if not session_row:
            return None
        session_dict = dict(session_row)
        return session_dict
