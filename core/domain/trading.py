from core.logger import get_logger
from core.sender import Sender
from core.ticker import Ticker, threading
from core.domain.account import Account
from core.domain.strategy import TradingStrategy
from core.domain.symbol import Symbol
from core.domain.session import TradingSession
from core.domain.order import Order, Fill
from core.domain.deposit_divider import DepositDivider
from datetime import datetime, timezone


logger = get_logger(__name__)
sender = Sender()


def get_percentage_difference(old_value, new_value):
    difference = new_value - old_value
    percentage_diff = ((difference / new_value) * 100)
    return percentage_diff


def add_percent(numeric_value, percent_value):
    percent = numeric_value * percent_value / 100
    price_with_percent = numeric_value + percent
    return price_with_percent


def attempt_make_deal(deposit_divider, account, trading_session, symbol, side, qty, price, deposit_batch, base_amount):
    logger.info(f"Attempt place order: {symbol.symbol}, {side}, price: {price}, qty: {qty}")

    new_order = Order(session_id=trading_session.session_id,
                      symbol=symbol,
                      side=side.upper(),
                      qty=qty,
                      price=price,
                      deposit_batch=deposit_batch,
                      base_amount=base_amount
                      )
    new_order.place_order()

    logger.info(f"Order {new_order.status}")

    if new_order.status == "FILLED":
        avg_fill_price = new_order.calculate_avg_fill_price()
        trading_session.last_action = side.upper()
        trading_session.average_cost_acquired_assets = 0 if side == "sell" else (
            trading_session.recalc_average_cost(new_order.executed_qty, avg_fill_price))
        trading_session.stage = 0 if side == "sell" else (
            trading_session.stage + 1)
        account.fill_data()
        trading_balances = account.get_trading_balances(symbol)
        trading_session.finish_base_amount = trading_balances["base_amount"]
        trading_session.finish_quote_amount = trading_balances["quote_amount"]
        deposit_divider.set_remnant(trading_session.finish_quote_amount)
        trading_session.save()


def continue_trading_session(account):
    if not account.can_trade:
        sender.send_message("Logic violation: account cant trade")
        raise RuntimeError("Logic violation: account cant trade")

    exemple_just_skip_tick = False
    if exemple_just_skip_tick:
        return False

    return True


def trading_cycle(ticker, deposit_divider, account,
                  trading_strategy: TradingStrategy, trading_session: TradingSession, symbol):

    # перевіряємо чи можна продовжувати
    if not continue_trading_session(account):
        return

    # Перевіряємо чи є оновлена стратегія. Якщо оновилась стратегія, то починаємо нову сесію
    # if trading_session.stage == 0:
    #     if trading_strategy.update_strategy():
    #         logger.info("Trading strategy has been updated. Stopping the current session to start new session")
    #         ticker.stop()
    #         run_trading(force_new_session=True)

    # Тут все починається торгівля
    avg_price = trading_session.get_avg_price()
    percentage_difference = get_percentage_difference(trading_session.average_cost_acquired_assets, avg_price)

    logger.debug(f"Tick, "
                 f"stage: {trading_session.stage}, "
                 f"avg cost: {trading_session.average_cost_acquired_assets}, "
                 f"avg price: {avg_price}, "
                 f"percentage difference: {round(percentage_difference, 2)}%")

    last_stage = trading_strategy.get_last_stage()

    if trading_session.stage > 0:
        """
        Якщо стейдж більше 0 то перевіримо чи середня ціна на ринку така,
        що допускає продаж (більша на відповідний відсоток від середньої вартості)
        """
        if percentage_difference > trading_strategy.percentage_min_profit:
            if trading_strategy.market_conditions_sufficient_to_action("sell"):
                price = trading_session.get_price_from_depth("sell", trading_session.finish_base_amount)
                if price:
                    logger.info(f"Остаточна ціна продажу: {price}")
                    # тут повторно перевіряємо чи влаштовує нас ціна продажу,
                    # і якщо так, отримуємо кінцеву кількість для ордера
                    percentage_difference = get_percentage_difference(trading_session.average_cost_acquired_assets,
                                                                      price)
                    logger.info(f"Остаточна відсоткова різниця: {round(percentage_difference, 2)}%")
                    if percentage_difference > trading_strategy.percentage_min_profit:
                        qty = trading_session.finish_base_amount
                        attempt_make_deal(deposit_divider=deposit_divider,
                                          account=account,
                                          trading_session=trading_session,
                                          symbol=symbol,
                                          side="sell",
                                          qty=qty,
                                          price=price,
                                          deposit_batch=0,
                                          base_amount=trading_session.finish_base_amount)

    if trading_session.stage <= last_stage:
        """
        Якщо стейдж менше останнього то перевіримо чи середня ціна на ринку така,
        що допускає покупку (менша на відповідний відсоток від середньої вартості, або це нульовий стейдж)
        """
        stage_parameters = trading_strategy.get_stage_parameters(trading_session.stage)
        if (percentage_difference < stage_parameters.price_change
                or trading_session.stage == 0):
            if trading_strategy.market_conditions_sufficient_to_action("buy"):
                deposit_batch = deposit_divider.get_batch(trading_session.stage)
                pre_qty = deposit_batch / avg_price
                price = trading_session.get_price_from_depth("buy", pre_qty)
                if price:
                    logger.info(f"Остаточна ціна купівлі: {price}")
                    # тут повторно перевіряємо чи влаштовує нас ціна купівлі,
                    # і якщо так, отримуємо кінцеву кількість для ордера
                    percentage_difference = get_percentage_difference(trading_session.average_cost_acquired_assets,
                                                                      price)
                    logger.info(f"Остаточна відсоткова різниця: {round(percentage_difference, 2)}%")
                    if (percentage_difference < stage_parameters.price_change
                            or trading_session.stage == 0):
                        qty = deposit_batch / avg_price
                        attempt_make_deal(deposit_divider=deposit_divider,
                                          account=account,
                                          trading_session=trading_session,
                                          symbol=symbol,
                                          side="buy",
                                          qty=qty,
                                          price=price,
                                          deposit_batch=deposit_batch,
                                          base_amount=0)


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
        deposit_divider = DepositDivider(trading_session.start_quote_amount,
                                         trading_strategy.get_batch_list())
    else:
        # пробуємо отримати дані про останню сесію з БД, також визначаємо яка була стратегія, та її також беремо з БД
        logger.info("Checking for an incomplete session...")
        trading_session = TradingSession()
        if trading_session.session_id > 0:
            logger.info(f"Incomplete session {trading_session.session_id} has been detected, restoring this session")
            trading_strategy = TradingStrategy(strategy_id=trading_session.strategy_id)
            symbol = Symbol(trading_strategy.symbol)
            symbol.fill_data()
            deposit_divider = DepositDivider(trading_session.finish_quote_amount,
                                             trading_strategy.get_batch_list())
        else:
            # якщо в БД даних немає, то починаємо нову сесію
            logger.info("Incomplete session not detected, starting a new session")
            trading_strategy, trading_session, symbol = start_new_session(account)
            deposit_divider = DepositDivider(trading_session.start_quote_amount,
                                             trading_strategy.get_batch_list())

    # далі все однаково для обох сценаріїв
    ticker = Ticker(10, trading_cycle,
                    deposit_divider=deposit_divider,
                    account=account,
                    trading_strategy=trading_strategy,
                    trading_session=trading_session,
                    symbol=symbol)
    thread = threading.Thread(target=ticker.start)
    thread.start()


def prepare_test_balances(target_amount=100):
    account = Account()
    account.fill_data()
    # продаємо весь BTC
    symbol_btc = Symbol("BTCUSDT")
    symbol_btc.fill_data()
    balances = account.get_trading_balances(symbol_btc)
    btc_amount = balances["base_amount"]
    usdt_amount = balances["quote_amount"]
    print(f"BTC: {btc_amount}, USDT: {usdt_amount}")
    if btc_amount > 0:
        order = Order(1, symbol_btc, "SELL", btc_amount, 0, 0, btc_amount, "MARKET")
        order.place_order()
        if order.status != "FILLED":
            print("BTC NOT продано")
            return
        print("Весь BTC продано")
        account.fill_data()
        symbol_btc.fill_data()
        balances = account.get_trading_balances(symbol_btc)
        btc_amount = balances["base_amount"]
        usdt_amount = balances["quote_amount"]
        print(f"BTC: {btc_amount}, USDT: {usdt_amount}")

    # купуємо або продаємо ETH, щоб лишилось близько цільової суми
    trade_amount = usdt_amount - target_amount
    if abs(trade_amount) < 11:
        # тоді так і лишаємо
        return

    symbol_eth = Symbol("ETHUSDT")
    symbol_eth.fill_data()
    balances = account.get_trading_balances(symbol_eth)
    eth_amount = balances["base_amount"]
    print(f"ETH: {eth_amount}, USDT: {usdt_amount}")

    trading_session = TradingSession(start_time=0, force_new_session=True)
    trading_session.symbol = "ETHUSDT"
    price = trading_session.get_avg_price()

    if usdt_amount > target_amount:
        qty = trade_amount / price
        order = Order(1, symbol_eth, "BUY", qty, 0, usdt_amount, 0, "MARKET")
        order.place_order()
        if order.status == "FILLED":
            print("Купили ETH майже на всі гроші")
        else:
            print("Не вдалось купити ETH майже на всі гроші")
    else:
        qty = abs(trade_amount) / price
        order = Order(1, symbol_eth, "SELL", qty, 0, 0, eth_amount, "MARKET")
        order.place_order()
        if order.status == "FILLED":
            print("Продали частку ETH")
        else:
            print("Не вдалось продати частку ETH")

    account.fill_data()
    # продаємо весь BTC
    symbol_btc = Symbol("BTCUSDT")
    symbol_btc.fill_data()
    balances = account.get_trading_balances(symbol_btc)
    btc_amount = balances["base_amount"]
    usdt_amount = balances["quote_amount"]
    print(f"BTC: {btc_amount}, USDT: {usdt_amount}")
