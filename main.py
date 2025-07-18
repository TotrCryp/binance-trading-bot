import logging
import argparse

from config import (DB_TESTING_STRATEGIES,
                    DB_TRADING,
                    START_DATE_COLLECTION_HISTORICAL_DATA,
                    AVAILABLE_SYMBOLS,
                    AVAILABLE_TIMEFRAMES,
                    AVAILABLE_MODES
                    )

from services.log import setup_logging

from db.sqlite_db import DbManager
from db.test_strat_db import CandlesDAO, TestResultsDAO
# from db.trading_db import ...DAO
from testing_strategies.data_preparation import HistoricalData
from testing_strategies.testing import Tester
from testing_strategies.strategy_preparation import Strategist
from api.market_data import CandlestickData


if __name__ == '__main__':

    setup_logging()

    parser = argparse.ArgumentParser(description="Coming soon...")
    parser.add_argument("-S", "--symbol",
                        required=True,
                        choices=AVAILABLE_SYMBOLS,
                        help="Trading instrument symbol - required parameter")
    parser.add_argument("-M", "--mode",
                        default="trading",
                        choices=AVAILABLE_MODES,
                        help="Mode trading or test (testing strategies)")
    parser.add_argument("-t", "--timeframe",
                        default="1h",
                        choices=AVAILABLE_TIMEFRAMES,
                        help="Timeframe for analysis and testing strategies - default 1h")
    parser.add_argument("-s", "--sandbox",
                        action="store_true",
                        help="All actions are performed in a sandbox (used for testing)")
    parser.add_argument("-u", "--update-historical-data",
                        action="store_true",
                        help="Update the historical data before testing strategies")

    args = parser.parse_args()

    symbol = args.symbol
    interval = args.timeframe
    mode = args.mode
    update_hd = args.update_historical_data
    sandbox = args.sandbox

    test_strat_db = DbManager(DB_TESTING_STRATEGIES)
    trading_db = DbManager(DB_TRADING)

    # Create DAO
    test_strat_db_connection = test_strat_db.get_connection()
    candle_dao = CandlesDAO(test_strat_db_connection, f"{symbol.lower()}_{interval}")
    test_result_dao = TestResultsDAO(test_strat_db_connection)

    # Ділянка оновлення історичних даних
    if update_hd:
        # todo винести це звідси в модуль оновлення історичних даних
        res_last_timestamp = candle_dao.get_last_timestamp()
        if res_last_timestamp is None:
            last_timestamp = START_DATE_COLLECTION_HISTORICAL_DATA * 1000
        else:
            last_timestamp = res_last_timestamp[0]
        api_candlestick_data = CandlestickData()
        historical_data = HistoricalData(symbol, interval)
        historical_data.update_kline_data(last_timestamp, candle_dao, api_candlestick_data)

    # Ділянка тестування стратегій
    if mode == "test":
        # todo винести це звідси в модуль тестування стратегій
        strategist = Strategist()
        strategy_set = strategist.get_strategy_set()
        for i, strategy in enumerate(strategy_set):
            tester = Tester(candle_dao, test_result_dao, symbol,
                            strategy["deposit_division_strategy"],
                            strategy["percentage_min_profit"],
                            strategy["market_indicators_strategy"])
            tester.run_test()
            logging.info(f"{i+1} of {len(strategy_set)} strategies tested ({round(((i+1)/len(strategy_set))*100, 3)}%)")

    # Close the connection on exit
    test_strat_db.close()
    trading_db.close()
