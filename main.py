from config import (DB_TESTING_STRATEGIES,
                    DB_TRADING,
                    START_DATE_COLLECTION_HISTORICAL_DATA,
                    setup_logging)

from db.sqlite_db import DbManager
from db.test_strat_db import CandlesDAO, TestResultsDAO
# from db.trading_db import ...DAO
from testing_strategies.data_preparation import HistoricalData
from testing_strategies.testing import Tester
from testing_strategies.strategy_preparation import Strategist
from api.market_data import CandlestickData


if __name__ == '__main__':

    setup_logging()

    symbol, interval = 'BTCUSDT', '1h'

    test_strat_db = DbManager(DB_TESTING_STRATEGIES)
    trading_db = DbManager(DB_TRADING)

    # Create DAO
    test_strat_db_connection = test_strat_db.get_connection()
    candle_dao = CandlesDAO(test_strat_db_connection, f"{symbol.lower()}_{interval}")
    test_result_dao = TestResultsDAO(test_strat_db_connection)

    # Ділянка оновлення історичних даних
    res_last_timestamp = candle_dao.get_last_timestamp()
    if res_last_timestamp is None:
        last_timestamp = START_DATE_COLLECTION_HISTORICAL_DATA * 1000
    else:
        last_timestamp = res_last_timestamp[0]
    api_candlestick_data = CandlestickData()
    historical_data = HistoricalData(symbol, interval)
    historical_data.update_kline_data(last_timestamp, candle_dao, api_candlestick_data)

    # Ділянка тестування стратегій
    strategist = Strategist()
    strategy_set = strategist.get_strategy_set()
    for strategy in strategy_set:
        tester = Tester(candle_dao, test_result_dao, symbol,
                        strategy["deposit_division_strategy"],
                        strategy["percentage_min_profit"],
                        strategy["market_indicators_strategy"])
        tester.run_test()

    # Close the connection on exit
    test_strat_db.close()
    trading_db.close()
