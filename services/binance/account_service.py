from api.binance.api_account import BinanceAccountAPI
from adapters.binance_adapter import AccountAdapter


class AccountService:
    def __init__(self):
        self.api = BinanceAccountAPI()

    def get_account(self):
        raw_data = self.api.get_account_info()
        return AccountAdapter.from_api(raw_data)
