from core.logger import get_logger
from core.sender import Sender
from core.domain.strategy import TradingStrategy
from core.domain.symbol import Symbol
from core.domain.session import TradingSession
from core.domain.order import Order, Fill


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
    якщо оновилась стратегія, то починаємо нову сесію
    """

    while True:
        if not continue_trading_session(account):
            continue

        pass

        # tick!!!

        # trading_session.last_action = "buy"
        # with db_helper.get_session() as db_session:
        #     repo = SessionRepository(db_session)
        #     trading_session = repo.save(trading_session)


def run_trading(force_new_session=False):
    if force_new_session:
        # якщо явно вказано почати нову сесію, то не потрібно отримувати дані про останню сесію з БД,
        # просто отримуємо стратегію та створюємо нову сесію
        trading_strategy = TradingStrategy()
        trading_session = TradingSession(start_time=1760000000)
        symbol = Symbol(trading_strategy.symbol)
        symbol.fill_data()
        trading_session.symbol = symbol.symbol
        trading_session.start_base_amount = 10
        trading_session.start_quote_amount = 0.0001
        trading_session.last_action = "START"
        trading_session.stage = 0
        trading_session.strategy_id = trading_strategy.strategy_id
        trading_session.save()
    else:
        # пробуємо отримати дані про останню сесію з БД, також визначаємо яка була стратегія, та її також беремо з БД
        trading_session = TradingSession()
        if trading_session.session_id > 0:
            trading_strategy = TradingStrategy(strategy_id=trading_session.strategy_id)
            symbol = Symbol(trading_strategy.symbol)
            symbol.fill_data()
        else:
            # якщо в БД даних немає, то починаємо нову сесію
            trading_strategy = TradingStrategy()
            symbol = Symbol(trading_strategy.symbol)
            symbol.fill_data()
            trading_session.symbol = symbol.symbol
            trading_session.start_base_amount = 10
            trading_session.start_quote_amount = 0.0001
            trading_session.last_action = "START"
            trading_session.stage = 0
            trading_session.strategy_id = trading_strategy.strategy_id
            trading_session.save()

    # далі все однаково для обох сценаріїв

    # new_order = Order(symbol=trading_session.symbol,
    #                   side="SELL",
    #                   order_type="LIMIT",
    #                   time_in_force="GTC",
    #                   session_id=trading_session.session_id)
    #
    # new_order.order_id = 1
    # new_order.order_list_id = 11
    # new_order.client_order_id = "myOrder001"
    # new_order.transact_time = 1725000000000
    # new_order.price = 68000.5
    # new_order.orig_qty = 1
    # new_order.executed_qty = 1
    # new_order.orig_quote_order_qty = 68000.5
    # new_order.cummulative_quote_qty = 68000.5
    # new_order.status = "FILLED"
    # new_order.working_time = 1725000000000
    #
    # fills = [
    #     Fill(price=78000, qty=0.6, commission=0.4, commission_asset="BTS", trade_id=234),
    #     Fill(price=79000, qty=0.4, commission=0.2, commission_asset="BNB", trade_id=1234)
    # ]
    #
    # new_order.fills = fills
    # new_order.save()

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
