from typing import List
from api.binance.api_exchange_Info import BinanceExchangeInfoAPI


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
        self.filters: List[dict] = []

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
        self.filters = symbol_data["filters"]

    def is_order_type_allowed(self, order_type: str) -> bool:
        return order_type.upper() in (t.upper() for t in self.order_types)

    def has_permission(self, permission: str) -> bool:
        p = permission.upper()
        return any(p in (perm.upper() for perm in perm_set) for perm_set in self.permission_sets)
