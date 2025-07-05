from config import (DB_TESTING_STRATEGIES,
                    DB_TRADING)

from db.sqlite_db import DbManager
from db.test_strat_db import CandlesDAO
# from db.trading_db import ...DAO


if __name__ == '__main__':
    test_strat_db = DbManager(DB_TESTING_STRATEGIES)
    trading_db = DbManager(DB_TRADING)

    # Create DAO
    candle_dao = CandlesDAO(test_strat_db.get_connection(), "f_table")
    # product_dao = ProductDAO(product_db.get_connection()

    # test requests
    candles = candle_dao.get_candles()
    # product = product_dao.get_product(5)

    print(candles)
    # print(product)

    # Close the connection on exit
    test_strat_db.close()
    trading_db.close()
