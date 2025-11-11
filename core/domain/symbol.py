from typing import List
from api.binance.api_exchange_Info import BinanceExchangeInfoAPI
from core.logger import get_logger

logger = get_logger(__name__)


class SymbolFilters:
    def __init__(self, filters: list[dict]):
        self.filters = {f["filterType"]: f for f in filters}

    @staticmethod
    def _float(value):
        return float(value) if isinstance(value, str) else value

    def adjust_price(self, price: float) -> float:
        f = self.filters.get("PRICE_FILTER")
        if not f:
            return price

        min_price = self._float(f["minPrice"])
        max_price = self._float(f["maxPrice"])
        tick_size = self._float(f["tickSize"])

        if price < min_price:
            price = min_price
        elif price > max_price:
            price = max_price

        # підгонка під tick_size (до найближчого кроку)
        if tick_size:
            steps = round((price - min_price) / tick_size)
            price = min_price + steps * tick_size
            # через похибку float краще округлити до кількості знаків після коми у tick_size
            decimals = len(f["tickSize"].split(".")[1].rstrip("0")) if "." in f["tickSize"] else 0
            price = round(price, decimals)

        return price

    def adjust_lot_size(self, quantity: float) -> float:
        f = self.filters.get("LOT_SIZE")
        if not f:
            return quantity

        min_qty = self._float(f["minQty"])
        max_qty = self._float(f["maxQty"])
        step_size = self._float(f["stepSize"])

        # обмеження в межах min/max
        if quantity < min_qty:
            quantity = min_qty
        elif quantity > max_qty:
            quantity = max_qty

        # підгонка під stepSize (до найближчого кроку)
        if step_size:
            steps = round((quantity - min_qty) / step_size)
            quantity = min_qty + steps * step_size
            # через похибку float краще округлити до кількості знаків після коми у stepSize
            decimals = len(f["stepSize"].split(".")[1].rstrip("0")) if "." in f["stepSize"] else 0
            quantity = round(quantity, decimals)

        return quantity

    def validate_min_notional(self, price: float, quantity: float):
        f = self.filters.get("MIN_NOTIONAL")
        if not f:
            return True
        min_notional = self._float(f["minNotional"])
        if price * quantity < min_notional:
            logger.warning(f"Notional {price * quantity} < minNotional {min_notional}")
            return False
        return True

    def get_step_size(self):
        f = self.filters.get("LOT_SIZE")
        if not f:
            return None
        return self._float(f["stepSize"])


class Symbol:
    def __init__(self, symbol):
        self.symbol: str = symbol
        self.status: str = ""
        self.base_asset: str = ""
        self.quote_asset: str = ""
        self.base_asset_precision: int = 0
        self.quote_asset_precision: int = 0
        self.base_commission_precision: int = 0
        self.quote_commission_precision: int = 0
        self.order_types: List[str] = []
        self.permission_sets: List[List[str]] = [[]]
        self.filters = None

    def fill_data(self):
        data = BinanceExchangeInfoAPI().get_exchange_info(self.symbol)
        symbol_data = data["symbols"][0]
        self.status = symbol_data["status"]
        self.base_asset = symbol_data["baseAsset"]
        self.quote_asset = symbol_data["quoteAsset"]
        self.base_asset_precision = symbol_data["baseAssetPrecision"]
        self.quote_asset_precision = symbol_data["quoteAssetPrecision"]
        self.base_commission_precision = symbol_data["baseCommissionPrecision"]
        self.quote_commission_precision = symbol_data["quoteCommissionPrecision"]
        self.order_types = symbol_data["orderTypes"]
        self.permission_sets = symbol_data["permissionSets"]
        self.filters = SymbolFilters(symbol_data["filters"])

    def is_order_type_allowed(self, order_type: str) -> bool:
        return order_type.upper() in (t.upper() for t in self.order_types)

    def has_permission(self, permission: str) -> bool:
        p = permission.upper()
        return any(p in (perm.upper() for perm in perm_set) for perm_set in self.permission_sets)
