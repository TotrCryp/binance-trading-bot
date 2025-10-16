from core.config import SYMBOL
from models import db_helper
from core.logger import get_logger
from core.domain.strategy import Strategy
from core.domain.session import TradingSession
from repositories import StrategyRepository, SessionRepository
from services.binance.account_service import AccountService
from services.binance.symbol_service import SymbolService

logger = get_logger(__name__)


def trading_cycle():
    while True:
        pass

        # trading_session.last_action = "buy"
        # with db_helper.get_session() as db_session:
        #     repo = SessionRepository(db_session)
        #     trading_session = repo.save(trading_session)


def run_trading():

    # orders

    service = SymbolService()
    symbol = service.get_exchange_info(SYMBOL)

    service = AccountService()
    account = service.get_account()

    strategy = Strategy()
    with db_helper.get_session() as db_session:
        repo = StrategyRepository(db_session)
        strategy = repo.save(strategy)

    trading_session = TradingSession(symbol=symbol.symbol,
                                     start_base_amount=0.0,
                                     start_quote_amount=0.0,
                                     stage=0,
                                     average_cost_acquired_assets=0.0,
                                     last_action="START",
                                     strategy=strategy)

    with db_helper.get_session() as db_session:
        repo = SessionRepository(db_session)
        trading_session = repo.save(trading_session)

    base_balance = next((b for b in account.balances if b.asset == symbol.base_asset), None)
    if base_balance is None:
        raise ValueError("Base balance is None")
    quote_balance = next((b for b in account.balances if b.asset == symbol.quote_asset), None)
    if quote_balance is None:
        raise ValueError("Quote balance is None")

    # base_balance.free

    if not account.can_trade:
        raise RuntimeError("Logic violation: account cant trade")

    trading_cycle()
