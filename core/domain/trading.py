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


def attempt_make_deal(account, trading_session, symbol, side, qty, price):
    logger.info(f"Attempt place order: {symbol.symbol}, {side}, price: {price}, qty: {qty}")

    new_order = Order(session_id=trading_session.session_id,
                      symbol=symbol,
                      side=side.upper(),
                      qty=qty,
                      price=price
                      )
    new_order.place_order()

    logger.info(f"Order {new_order.status}")

    if new_order.status == "FILLED":
        avg_fill_price = new_order.calculate_avg_fill_price()
        trading_session.last_action = side.upper()
        trading_session.average_cost_acquired_assets = 0 if side == "sell" else (
            trading_session.recalc_average_cost(new_order.executed_qty, avg_fill_price))
        # account.fill_data()
        # trading_balances = account.get_trading_balances(symbol)
        # trading_session.finish_base_amount = trading_balances["base_amount"]
        # trading_session.finish_quote_amount = trading_balances["quote_amount"]
        trading_session.finish_base_amount += new_order.executed_qty
        trading_session.finish_quote_amount -= new_order.executed_qty * avg_fill_price
        trading_session.save()


def continue_trading_session(account):
    if not account.can_trade:
        sender.send_message("Logic violation: account cant trade")
        raise RuntimeError("Logic violation: account cant trade")

    exemple_just_skip_tick = False
    if exemple_just_skip_tick:
        return False

    return True


def trading_cycle(ticker, account, trading_strategy: TradingStrategy, trading_session: TradingSession, symbol):

    # перевіряємо чи можна продовжувати
    if not continue_trading_session(account):
        return

    # Перевіряємо чи є оновлена стратегія. Якщо оновилась стратегія, то починаємо нову сесію
    if trading_session.stage == 0:
        if trading_strategy.update_strategy():
            logger.info("Trading strategy has been updated. Stopping the current session to start new session")
            ticker.stop()
            run_trading(force_new_session=True)

    # Тут все починається торгівля
    # if trading_session.last_action == "BUY":
    #     price = trading_session.get_price_from_depth("sell", 0.001)
    #     if price:
    #         pass
    #         # attempt_make_deal(account, trading_session, symbol, side, qty, price)
    # else:
    #     price = trading_session.get_price_from_depth("buy", 0.001)
    #     if price:
    #         pass

    print("tick")
    price = trading_session.get_price_from_depth("buy", 0.001)
    if trading_session.average_cost_acquired_assets > 0:
        if price < trading_session.average_cost_acquired_assets:
            attempt_make_deal(account, trading_session, symbol, "buy", 0.001, price)
    else:
        attempt_make_deal(account, trading_session, symbol, "buy", 0.001, price)

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
