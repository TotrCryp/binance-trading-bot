from core.logger import get_logger
from core.sender import Sender
from core.domain.strategy import TradingStrategy
from core.domain.symbol import Symbol
# from core.domain.order import Order
# from db import trading_session


logger = get_logger(__name__)
sender = Sender()


def continue_trading_session(account):
    if not account.can_trade:
        sender.send_message("Logic violation: account cant trade")
        raise RuntimeError("Logic violation: account cant trade")


def trading_cycle(account):
    a = 1

    """
    перевіряємо чи можна продовжувати
    перевіряємо чи є оновлена стратегія
    """

    while True:
        if not continue_trading_session(account):
            continue

        pass

        # tick

        # trading_session.last_action = "buy"
        # with db_helper.get_session() as db_session:
        #     repo = SessionRepository(db_session)
        #     trading_session = repo.save(trading_session)


def run_trading(restore=True):
    trading_strategy = TradingStrategy(strategy_id=1)
    symbol = Symbol(trading_strategy.symbol)
    symbol.fill_data()

    d = 1

    # orders
    # temp_test_order()
    #
    # service = SymbolService()
    # symbol = service.get_exchange_info(SYMBOL)
    #
    # service = AccountService()
    # account = service.get_account()
    #
    # strategy = Strategy()
    # with db_helper.get_session() as db_session:
    #     repo = StrategyRepository(db_session)
    #     strategy = repo.save(strategy)
    #
    # trading_session = TradingSession(symbol=symbol.symbol,
    #                                  start_base_amount=0.0,
    #                                  start_quote_amount=0.0,
    #                                  stage=0,
    #                                  average_cost_acquired_assets=0.0,
    #                                  last_action="START",
    #                                  strategy=strategy)
    #
    # with db_helper.get_session() as db_session:
    #     repo = SessionRepository(db_session)
    #     trading_session = repo.save(trading_session)
    #
    # base_balance = next((b for b in account.balances if b.asset == symbol.base_asset), None)
    # if base_balance is None:
    #     raise ValueError("Base balance is None")
    # quote_balance = next((b for b in account.balances if b.asset == symbol.quote_asset), None)
    # if quote_balance is None:
    #     raise ValueError("Quote balance is None")
    # base_amount = base_balance.free
    # quote_amount = quote_balance.free
    #
    # trading_cycle(account)
