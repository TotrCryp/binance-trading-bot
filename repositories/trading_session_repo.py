from models import TradingSessionORM, TradingStrategyORM
from core.domain.session import TradingSession
from core.mixins import ORMConvertibleMixin
from sqlalchemy.orm import Session
from core.logger import get_logger

logger = get_logger(__name__)


class SessionRepository(ORMConvertibleMixin):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def trading_session_to_orm(self, trading_session) -> TradingSessionORM:
        orm_obj = self.to_orm(TradingSessionORM, trading_session)
        return orm_obj

    def save(self, trading_session: TradingSession) -> TradingSession:
        if trading_session.id:
            orm_obj = self.db_session.get(TradingSessionORM, trading_session.id)
            orm_obj.stage = trading_session.stage
            orm_obj.average_cost_acquired_assets = trading_session.average_cost_acquired_assets
            orm_obj.last_action = trading_session.last_action
        else:
            #  Отримуємо ORM-об’єкт стратегії
            strategy_orm = self.db_session.get(TradingStrategyORM, trading_session.strategy.id)
            orm_obj = self.trading_session_to_orm(trading_session)
            orm_obj.trading_strategy = strategy_orm

        self.db_session.add(orm_obj)
        self.db_session.commit()
        self.db_session.refresh(orm_obj)
        logger.info("Trading session data has been saved")
        trading_session.id = orm_obj.id
        return trading_session
