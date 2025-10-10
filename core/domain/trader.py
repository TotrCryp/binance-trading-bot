class Trader:
    def __init__(self, symbol):
        self._symbol = symbol
        self._base_amount = 1000.00
        self._quote_amount = 0.00
        self._average_cost = 0
        self._stage = 0
        self._last_price = 0
