from core.domain.account import Account, Balance, CommissionRates
from core.domain.symbol import Symbol
from datetime import datetime


class AccountAdapter:
    @staticmethod
    def from_api(data: dict) -> Account:
        commission_rates = CommissionRates(
            maker=float(data["commissionRates"]["maker"]),
            taker=float(data["commissionRates"]["taker"]),
            buyer=float(data["commissionRates"]["buyer"]),
            seller=float(data["commissionRates"]["seller"]),
        )

        balances = [
            Balance(
                asset=item["asset"],
                free=float(item["free"]),
                locked=float(item["locked"])
            )
            for item in data["balances"]
        ]

        account = Account(
            uid=data["uid"],
            account_type=data["accountType"],
            can_trade=data["canTrade"],
            can_withdraw=data["canWithdraw"],
            can_deposit=data["canDeposit"],
            update_time=datetime.fromtimestamp(data["updateTime"] / 1000),
            commission_rates=commission_rates,
            balances=balances
        )

        return account


class SymbolAdapter:
    @staticmethod
    def from_api(data: dict) -> Symbol:
        if len(data["symbols"]) != 1:
            raise RuntimeError("Logic violation: some problem with Symbol in ExchangeInfo")

        symbol_data = data["symbols"][0]

        filters = [
            item
            for item in symbol_data["filters"]
        ]

        symbol = Symbol(
            symbol=symbol_data["symbol"],
            status=symbol_data["status"],
            base_asset=symbol_data["baseAsset"],
            quote_asset=symbol_data["quoteAsset"],
            base_asset_precision=symbol_data["baseAssetPrecision"],
            quote_asset_precision=symbol_data["quoteAssetPrecision"],
            base_commission_precision=symbol_data["baseCommissionPrecision"],
            quote_commission_precision=symbol_data["quoteCommissionPrecision"],
            order_types=symbol_data["orderTypes"],
            permission_sets=symbol_data["permissionSets"],
            filters=filters
        )

        return symbol
