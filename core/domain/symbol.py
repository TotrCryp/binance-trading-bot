from dataclasses import dataclass
from typing import List


@dataclass
class Symbol:
    symbol: str
    status: str
    base_asset: str
    quote_asset: str
    base_asset_precision: int
    quote_asset_precision: int
    base_commission_precision: int
    quote_commission_precision: int
    order_types: List[str]
    permission_sets: List[List[str]]
    filters: List[dict]

    def is_order_type_allowed(self, order_type: str) -> bool:
        return order_type.upper() in (t.upper() for t in self.order_types)

    def has_permission(self, permission: str) -> bool:
        p = permission.upper()
        return any(p in (perm.upper() for perm in perm_set) for perm_set in self.permission_sets)
