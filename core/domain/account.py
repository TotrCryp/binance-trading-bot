from core.logger import get_logger
from core.sender import Sender
from dataclasses import dataclass
from typing import List
from datetime import datetime
from api.binance.api_account import BinanceAccountAPI


logger = get_logger(__name__)
sender = Sender()


@dataclass
class CommissionRates:
    maker: float
    taker: float
    buyer: float
    seller: float


@dataclass
class Balance:
    asset: str
    free: float
    locked: float


class Account:
    def __init__(self):
        self.uid: int | None = None
        self.account_type: str | None = None
        self.can_trade: bool = False
        self.can_withdraw: bool = False
        self.can_deposit: bool = False
        self.update_time: datetime | None = None
        self.commission_rates: CommissionRates | None = None
        self.balances: List[Balance] = []
        self.permissions: List[str] = []

    def fill_data(self):
        data = BinanceAccountAPI().get_account_info()

        self.uid = data["uid"]
        self.account_type = data["accountType"]
        self.can_trade = data["canTrade"]
        self.can_withdraw = data["canWithdraw"]
        self.can_deposit = data["canDeposit"]
        self.update_time = datetime.fromtimestamp(data["updateTime"] / 1000)

        # CommissionRates
        commission = data.get("commissionRates", {})
        self.commission_rates = CommissionRates(
            maker=float(commission.get("maker", 0)),
            taker=float(commission.get("taker", 0)),
            buyer=float(commission.get("buyer", 0)),
            seller=float(commission.get("seller", 0)),
        )

        # Balances
        self.balances = [
            Balance(
                asset=item["asset"],
                free=float(item["free"]),
                locked=float(item["locked"]),
            )
            for item in data.get("balances", [])
        ]

        # Permissions
        self.permissions = [
            item for item in data.get("permissions", [])
        ]

    def get_trading_balances(self, symbol):
        base_balance = next((b for b in self.balances if b.asset == symbol.base_asset), None)
        if base_balance is None:
            base_amount = 0
        else:
            base_amount = base_balance.free
        quote_balance = next((b for b in self.balances if b.asset == symbol.quote_asset), None)
        if quote_balance is None:
            quote_amount = 0
        else:
            quote_amount = quote_balance.free

        if quote_amount == 0 and base_amount == 0:
            sender.send_message("ValueError: All balances have a zero value")
            raise ValueError("All balances have a zero value")

        return {
            "base_amount": base_amount,
            "quote_amount": quote_amount,
        }
