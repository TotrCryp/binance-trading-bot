from typing import List
from core.logger import get_logger
from core.domain.symbol import Symbol
from db.order import save
from api.binance.api_order import BinanceOrderAPI

logger = get_logger(__name__)


class Fill:
    def __init__(self, price: str, qty: str, commission: str, commission_asset: str, trade_id: int):
        self.price: float = float(price)
        self.qty: float = float(qty)
        self.commission: float = float(commission)
        self.commission_asset: str = commission_asset
        self.trade_id: int = trade_id


class Order:
    def __init__(self, session_id: int,
                 symbol: Symbol,
                 side: str,
                 qty: float,
                 price: float,
                 deposit_batch: float,
                 order_type: str = "LIMIT",
                 time_in_force: str = "FOK"):
        self.order_id: int = 0
        self._obj_symbol = symbol
        self._deposit_batch = deposit_batch
        self.symbol: str = symbol.symbol
        self.order_list_id: int = 0
        self.client_order_id: str = ""
        self.transact_time: int = 0
        self.price: float = self._obj_symbol.filters.adjust_price(price)
        self.orig_qty: float = self._obj_symbol.filters.adjust_lot_size(qty)
        self.adjust_qty_according_deposit_batch()
        self.executed_qty: float = 0.0
        self.orig_quote_order_qty: float = 0.0
        self.cummulative_quote_qty: float = 0.0
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
                if key == "fills" and isinstance(value, list):
                    self.fills = [
                        Fill(
                            price=f.get("price"),
                            qty=f.get("qty"),
                            commission=f.get("commission"),
                            commission_asset=f.get("commissionAsset"),
                            trade_id=f.get("tradeId"),
                        )
                        for f in value
                    ]
                    continue
                attr_name = self._to_attr_name(key)
                # if hasattr(self, attr_name):
                #     setattr(self, attr_name, value)

                if hasattr(self, attr_name):
                    current_type = type(getattr(self, attr_name))
                    if current_type is float and isinstance(value, str):
                        value = float(value)
                    elif current_type is int and isinstance(value, str) and value.isdigit():
                        value = int(value)
                    setattr(self, attr_name, value)

            self.save()

    def adjust_qty_according_deposit_batch(self):
        logger.debug(f"Коригування відповідно до частки депозиту {self._deposit_batch}, ціна {self.price}")
        logger.debug(f"Кількість до коригування: {self.orig_qty}")
        step_size = self._obj_symbol.filters.get_step_size()
        if step_size:
            while self._deposit_batch < self.price * self.orig_qty:
                self.orig_qty -= step_size
        logger.debug(f"Кількість після коригування: {self.orig_qty}")

    def calculate_avg_fill_price(self) -> float:
        total_qty = sum(f.qty for f in self.fills)
        if not total_qty:
            return 0.0
        total_value = sum(f.price * f.qty for f in self.fills)
        return total_value / total_qty

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
