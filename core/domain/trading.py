from core.config import SYMBOL
from models import db_helper, TradingStrategyORM
from core.logger import get_logger
from core.domain.strategy import Strategy
from core.domain.session import TradingSession
from repositories import StrategyRepository, SessionRepository

logger = get_logger(__name__)


def run_trading():

    strategy = Strategy()
    with db_helper.get_session() as db_session:
        repo = StrategyRepository(db_session)
        strategy = repo.save(strategy)

    trading_session = TradingSession(symbol=SYMBOL,
                                     start_base_amount=0.5,
                                     start_quote_amount=1000,
                                     stage=0,
                                     average_cost_acquired_assets=0.0,
                                     last_action="START",
                                     strategy=strategy)

    with db_helper.get_session() as db_session:
        repo = SessionRepository(db_session)
        trading_session = repo.save(trading_session)

    # trading_session.last_action = "buy"
    # with db_helper.get_session() as db_session:
    #     repo = SessionRepository(db_session)
    #     trading_session = repo.save(trading_session)
