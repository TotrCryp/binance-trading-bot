from typing import List
from core.logger import get_logger
from db.order import save
from api.binance.api_order import BinanceOrderAPI

logger = get_logger(__name__)


class Fill:
    def __init__(self, price: float, qty: float, commission: float, commission_asset: str, trade_id: int):
        self.price: float = price
        self.qty: float = qty
        self.commission: float = commission
        self.commission_asset: str = commission_asset
        self.trade_id: int = trade_id


class Order:
    def __init__(self, session_id: int,
                 symbol: str,
                 side: str,
                 qty: float,
                 price: float,
                 order_type: str = "LIMIT",
                 time_in_force: str = "FOK"):
        self.order_id: int = 0
        self.symbol: str = symbol
        self.order_list_id: int = 0
        self.client_order_id: str = ""
        self.transact_time: int = 0
        self.price: float = price
        self.orig_qty: float = qty
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

    def place_order(self):
        result = BinanceOrderAPI().post_order(self.symbol,
                                              self.side,
                                              self.orig_qty,
                                              self.price,
                                              self.type,
                                              self.time_in_force)
        if result and isinstance(result, dict):
            for key, value in result.items():
                attr_name = self._to_attr_name(key)
                if hasattr(self, attr_name):
                    setattr(self, attr_name, value)

    @staticmethod
    def _to_attr_name(api_key: str) -> str:
        mapping = {
            "orderId": "order_id",
            "orderListId": "order_list_id",
            "clientOrderId": "client_order_id",
            "transactTime": "transact_time",
            "origQty": "orig_qty",
            "executedQty": "executed_qty",
            "origQuoteOrderQty": "orig_quote_order_qty",
            "cummulativeQuoteQty": "cummulative_quote_qty",
            "timeInForce": "time_in_force",
            "workingTime": "working_time",
        }
        return mapping.get(api_key, api_key)

    def save(self):
        order_id = save(self)
        self.order_id = order_id
