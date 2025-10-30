from db.service import get_db


def save(order):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO orders (
                order_id, symbol, order_list_id, client_order_id, transact_time,
                price, orig_qty, executed_qty, orig_quote_order_qty, cummulative_quote_qty,
                status, time_in_force, type, side, working_time, session_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            order.order_id, order.symbol, order.order_list_id, order.client_order_id, order.transact_time,
            order.price, order.orig_qty, order.executed_qty, order.orig_quote_order_qty, order.cummulative_quote_qty,
            order.status, order.time_in_force, order.type, order.side, order.working_time, order.session_id
        ))

        for fill in order.fills:
            cursor.execute("""
                INSERT INTO fills (
                    order_id, price, qty, commission, commission_asset, trade_id
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                order.order_id, fill.price, fill.qty,
                fill.commission, fill.commission_asset, fill.trade_id
            ))

        conn.commit()


def get(order_id: int):
    pass
