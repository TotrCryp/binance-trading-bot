import logging
import argparse
import os

from config import (DB_TESTING_STRATEGIES,
                    DB_TRADING,
                    START_DATE_COLLECTION_HISTORICAL_DATA,
                    AVAILABLE_SYMBOLS,
                    AVAILABLE_TIMEFRAMES,
                    AVAILABLE_MODES
                    )

from services.log import setup_logging
from services.messenger_notifications import Notifier

from db.sqlite_db import DbManager
from db.test_strat_db import CandlesDAO, TestResultsDAO
# from db.trading_db import ...DAO
from testing_strategies.data_preparation import HistoricalData
from testing_strategies.testing import Tester
from testing_strategies.strategy_preparation import Strategist
from api.market_data import CandlestickData
from api.telegram import TelegramAPI


def perform_update_historical_data(symbol, interval):
    res_last_timestamp = candle_dao.get_last_timestamp()
    if res_last_timestamp is None:
        last_timestamp = START_DATE_COLLECTION_HISTORICAL_DATA * 1000
    else:
        last_timestamp = res_last_timestamp[0]
    api_candlestick_data = CandlestickData()
    historical_data = HistoricalData(symbol, interval)
    historical_data.update_kline_data(last_timestamp, candle_dao, api_candlestick_data)


def start_in_test_mode(symbol):
    strategist = Strategist()
    strategy_set = strategist.get_strategy_set()
    for i, strategy in enumerate(strategy_set):
        tester = Tester(candle_dao, test_result_dao, symbol,
                        strategy["deposit_division_strategy"],
                        strategy["percentage_min_profit"],
                        strategy["market_indicators_strategy"])
        tester.run_test()
        logging.info(
            f"{i + 1} of {len(strategy_set)} strategies tested ({round(((i + 1) / len(strategy_set)) * 100, 3)}%)")


def start_in_trading_mode():
    pass


def process_startup_arguments():
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

    return parser.parse_args()


if __name__ == '__main__':

    setup_logging()

    args = process_startup_arguments()

    # Create Telegram class for Notifier
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    telegram_owner_chat_id = os.getenv("TELEGRAM_OWNER_CHAT_ID")
    telegram = TelegramAPI(telegram_token, telegram_owner_chat_id)

    # Create Notifier class for sending messages
    notifier = Notifier(telegram)
    notifier.notify("Hello from Notifier")

    # Databases
    test_strat_db = DbManager(DB_TESTING_STRATEGIES)
    trading_db = DbManager(DB_TRADING)

    # Create DAO
    test_strat_db_connection = test_strat_db.get_connection()
    candle_dao = CandlesDAO(test_strat_db_connection, f"{args.symbol.lower()}_{args.timeframe}")
    test_result_dao = TestResultsDAO(test_strat_db_connection)

    # Ділянка оновлення історичних даних
    if args.update_historical_data:
        perform_update_historical_data(args.symbol, args.timeframe)

    # Ділянка тестування стратегій
    if args.mode == "test":
        start_in_test_mode(args.symbol)

    # Ділянка торгівлі
    if args.mode == "trading":
        start_in_trading_mode()

    # Close the connection on exit
    test_strat_db.close()
    trading_db.close()
