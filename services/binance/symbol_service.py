from api.binance.api_general import BinanceExchangeInfoAPI
from adapters.binance_adapter import SymbolAdapter


class SymbolService:
    def __init__(self):
        self.api = BinanceExchangeInfoAPI()

    def get_exchange_info(self, symbol):
        raw_data = self.api.get_exchange_info(symbol)
        return SymbolAdapter.from_api(raw_data)
