from core.sender import Sender
from core.logger import get_logger
from db.trading_session import save, update, get, get_last_id
from api.binance.api_depth import BinanceDepthAPI
from api.binance.api_book_ticker import BinanceBookTickerAPI
from api.binance.api_avg_price import BinanceAvgPriceAPI

sender = Sender()
logger = get_logger(__name__)


class TradingSession:
    def __init__(self, force_new_session=False, start_time=0):
        self.session_id: int = 0
        if force_new_session:
            self.symbol: str = ""
            self.start_base_amount: float = 0
            self.start_quote_amount: float = 0
            self.finish_base_amount: float = 0
            self.finish_quote_amount: float = 0
            self.stage: int = 0
            self.average_cost_acquired_assets: float = 0
            self.last_action: str = ""
            self.strategy_id: int = 0
            self.start_time: int = start_time
        else:
            last_id = get_last_id()
            if last_id:
                self.session_id: int = last_id
                self.get()

    def save(self):
        if self.session_id == 0:
            session_id = save(self)
            self.session_id = session_id
            logger.info("Session has been saved")
        else:
            update(self)
            logger.info("Session has been updated")

    def get(self):
        session_dict = get(self.session_id)
        if session_dict is None:
            sender.send_message(f"Trading session with id {self.session_id} not found")
            raise LookupError(f"Trading session with id {self.session_id} not found")
        self.load_from_dict(session_dict)

    def load_from_dict(self, session_dict):
        for key, value in session_dict.items():
            setattr(self, key, value)

    def get_avg_price(self) -> float:
        avg_price_data = BinanceAvgPriceAPI().get_avg_price(self.symbol)
        return float(avg_price_data["price"])

    def get_price_from_depth(self, side: str, quantity: float, ) -> float | None:
        # Спочатку спробуємо отримати ціну меншою вагою через bookTicker
        book_ticker = BinanceBookTickerAPI().get_book_ticker(self.symbol)
        price = book_ticker["bidPrice"] if side == "sell" else book_ticker["askPrice"]
        qty = book_ticker["bidQty"] if side == "sell" else book_ticker["askQty"]
        if float(qty) > quantity:
            return float(price)
        # Якщо ні, то отримуємо книгу ордерів
        depth_data = BinanceDepthAPI().get_depth(self.symbol)
        # Якщо продаємо — беремо покупців (bids), починаючи з найвищої ціни.
        # Якщо купуємо — беремо продавців (asks), починаючи з найнижчої.
        book = depth_data["bids"] if side == "sell" else depth_data["asks"]

        remaining = quantity
        total_cost = 0.0
        total_acquired = 0.0

        for price_str, qty_str in book:
            price = float(price_str)
            avail = float(qty_str)

            if remaining <= 0:
                break

            trade_qty = min(remaining, avail)
            total_cost += trade_qty * price
            total_acquired += trade_qty
            remaining -= trade_qty

        if remaining > 0:
            # Якщо в стакані не вистачає об’єму — значить, ціна не визначається.
            logger.warn("There is not enough volume in order book for the given quantity")
            return None

        return total_cost / total_acquired

    def recalc_average_cost(self, new_qty, new_avg_price) -> float:
        logger.info("Recalc:")
        logger.info(f"new_qty: {new_qty}, new_avg_price: {new_avg_price}")
        new_total_value = new_qty * new_avg_price
        logger.info(f"new_total_value: {new_total_value}")
        logger.info(f"finish_base_amount: {self.finish_base_amount}, "
                    f"average_cost_acquired_assets: {self.average_cost_acquired_assets}")
        old_total_value = self.finish_base_amount * self.average_cost_acquired_assets
        logger.info(f"old_total_value: {old_total_value}")
        total_qty = self.finish_base_amount + new_qty
        logger.info(f"total_qty: {total_qty}")
        logger.info(f"result: {(old_total_value + new_total_value) / total_qty}")
        return (old_total_value + new_total_value) / total_qty
