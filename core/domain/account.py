from dataclasses import dataclass
from typing import List
from datetime import datetime


@dataclass
class Balance:
    asset: str
    free: float
    locked: float


@dataclass
class CommissionRates:
    maker: float
    taker: float
    buyer: float
    seller: float


@dataclass
class Account:
    uid: int
    account_type: str
    can_trade: bool
    can_withdraw: bool
    can_deposit: bool
    update_time: datetime
    commission_rates: CommissionRates
    balances: List[Balance]
