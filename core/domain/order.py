from typing import List
from core.logger import get_logger
from db.order import save

logger = get_logger(__name__)


class Fill:
    def __init__(self, price: float, qty: float, commission: float, commission_asset: str, trade_id: int):
        self.price: float = price
        self.qty: float = qty
        self.commission: float = commission
        self.commission_asset: str = commission_asset
        self.trade_id: int = trade_id


class Order:
    def __init__(self, symbol: str, side: str, order_type: str, time_in_force: str, session_id: int):
        self.order_id: int = 0
        self.symbol: str = symbol
        self.order_list_id: int = 0
        self.client_order_id: str = ""
        self.transact_time: int = 0
        self.price: float = 0
        self.orig_qty: float = 0
        self.executed_qty: float = 0
        self.orig_quote_order_qty: float = 0
        self.cummulative_quote_qty: float = 0
        self.status: str = ""
        self.time_in_force: str = time_in_force
        self.type: str = order_type
        self.side: str = side
        self.working_time: int = 0
        self.session_id = session_id
        self.fills: List[Fill] = []

    def save(self):
        order_id = save(self)
        self.order_id = order_id
