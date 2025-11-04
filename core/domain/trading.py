from core.logger import get_logger
from core.sender import Sender
from core.ticker import Ticker, threading
from core.domain.account import Account
from core.domain.strategy import TradingStrategy
from core.domain.symbol import Symbol
from core.domain.session import TradingSession
from core.domain.order import Order, Fill
from datetime import datetime, timezone


logger = get_logger(__name__)
sender = Sender()


def some_about_order(trading_session):
    new_order = Order(symbol=trading_session.symbol,
                      side="SELL",
                      order_type="LIMIT",
                      time_in_force="GTC",
                      session_id=trading_session.session_id)

    new_order.order_id = 1
    new_order.order_list_id = 11
    new_order.client_order_id = "myOrder001"
    new_order.transact_time = 1725000000000
    new_order.price = 68000.5
    new_order.orig_qty = 1
    new_order.executed_qty = 1
    new_order.orig_quote_order_qty = 68000.5
    new_order.cummulative_quote_qty = 68000.5
    new_order.status = "FILLED"
    new_order.working_time = 1725000000000

    fills = [
        Fill(price=78000, qty=0.6, commission=0.4, commission_asset="BTS", trade_id=234),
        Fill(price=79000, qty=0.4, commission=0.2, commission_asset="BNB", trade_id=1234)
    ]

    new_order.fills = fills
    new_order.save()


def continue_trading_session(account):
    if not account.can_trade:
        sender.send_message("Logic violation: account cant trade")
        raise RuntimeError("Logic violation: account cant trade")

    exemple_just_skip_tick = False
    if exemple_just_skip_tick:
        return False

    return True


def trading_cycle(ticker, account, trading_strategy, trading_session, symbol):
    """
    перевіряємо чи є оновлена стратегія
    якщо оновилась стратегія, то починаємо нову сесію
    """

    # перевіряємо чи можна продовжувати
    if not continue_trading_session(account):
        return
    print("Tick:", trading_strategy, trading_session, symbol)

    # ticker.stop()


def start_new_session(account):
    now_utc = datetime.now(timezone.utc)
    unix_time = int(now_utc.timestamp())
    trading_strategy = TradingStrategy()
    trading_session = TradingSession(start_time=unix_time, force_new_session=True)
    symbol = Symbol(trading_strategy.symbol)
    symbol.fill_data()
    trading_session.symbol = symbol.symbol
    trading_balances = account.get_trading_balances(symbol)
    trading_session.start_base_amount = trading_balances["base_amount"]
    trading_session.start_quote_amount = trading_balances["quote_amount"]
    trading_session.last_action = "START"
    trading_session.stage = 0
    trading_session.strategy_id = trading_strategy.strategy_id
    trading_session.save()
    return trading_strategy, trading_session, symbol


def run_trading(force_new_session=False):
    account = Account()
    account.fill_data()
    if force_new_session:
        # якщо явно вказано почати нову сесію, то не потрібно отримувати дані про останню сесію з БД,
        logger.info("Launch with the 'force_new_session' parameter, forcibly starting a new session")
        trading_strategy, trading_session, symbol = start_new_session(account)
    else:
        # пробуємо отримати дані про останню сесію з БД, також визначаємо яка була стратегія, та її також беремо з БД
        logger.info("Checking for an incomplete session...")
        trading_session = TradingSession()
        if trading_session.session_id > 0:
            logger.info(f"Incomplete session {trading_session.session_id} has been detected, restoring this session")
            trading_strategy = TradingStrategy(strategy_id=trading_session.strategy_id)
            symbol = Symbol(trading_strategy.symbol)
            symbol.fill_data()
        else:
            # якщо в БД даних немає, то починаємо нову сесію
            logger.info("No incomplete session detected, starting a new session")
            trading_strategy, trading_session, symbol = start_new_session(account)

    # далі все однаково для обох сценаріїв
    ticker = Ticker(10, trading_cycle,
                    account=account,
                    trading_strategy=trading_strategy,
                    trading_session=trading_session,
                    symbol=symbol)
    thread = threading.Thread(target=ticker.start)
    thread.start()
