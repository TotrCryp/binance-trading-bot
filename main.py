from config import (DB_TESTING_STRATEGIES,
                    DB_TRADING,
                    START_DATE_COLLECTION_HISTORICAL_DATA)

from db.sqlite_db import DbManager
from db.test_strat_db import CandlesDAO
# from db.trading_db import ...DAO
from testing_strategies.data_preparation import HistoricalData
from api.market_data import CandlestickData


if __name__ == '__main__':

    symbol, interval = 'BTCUSDT', '1h'

    test_strat_db = DbManager(DB_TESTING_STRATEGIES)
    trading_db = DbManager(DB_TRADING)

    # Create DAO
    candle_dao = CandlesDAO(test_strat_db.get_connection(), f"{symbol.lower()}_{interval}")
    res_last_timestamp = candle_dao.get_last_timestamp()
    if res_last_timestamp is None:
        last_timestamp = START_DATE_COLLECTION_HISTORICAL_DATA * 1000
    else:
        last_timestamp = res_last_timestamp[0]
    api_candlestick_data = CandlestickData()
    historical_data = HistoricalData(symbol, interval)
    historical_data.update_kline_data(last_timestamp, candle_dao, api_candlestick_data)
    # product_dao = ProductDAO(product_db.get_connection()

    # test requests
    # candles = candle_dao.get_candles()
    # product = product_dao.get_product(5)

    # print(product)

    # Close the connection on exit
    test_strat_db.close()
    trading_db.close()
