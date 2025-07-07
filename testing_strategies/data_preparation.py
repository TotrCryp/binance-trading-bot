class HistoricalData:
    def __init__(self, symbol, interval):
        self._symbol = symbol
        self._interval = interval

    def update_kline_data(self, last_timestamp, candle_dao, api_candlestick_data):
        start_time = last_timestamp
        keep_updating = True
        while keep_updating:
            dataset = api_candlestick_data.get_kline_data(self._symbol, self._interval, start_time)
            if dataset:
                candle_dao.set_candles(dataset)
                start_time = dataset[-1][6]
            keep_updating = len(dataset) == 1000
