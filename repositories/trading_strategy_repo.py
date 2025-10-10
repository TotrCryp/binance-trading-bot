from models import TradingStrategyORM
from core.domain.strategy import Strategy
from core.mixins import ORMConvertibleMixin
from sqlalchemy.orm import Session
from core.logger import get_logger

logger = get_logger(__name__)


class StrategyRepository(ORMConvertibleMixin):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def strategy_to_orm(self, strategy) -> TradingStrategyORM:
        orm_obj = self.to_orm(TradingStrategyORM, strategy)
        if hasattr(strategy, "deposit_division_strategy"):
            orm_obj.deposit_division_strategy = [
                part.model_dump() for part in strategy.deposit_division_strategy
            ]
        return orm_obj

    def save(self, strategy: Strategy) -> Strategy:
        orm_obj = self.strategy_to_orm(strategy)
        self.db_session.add(orm_obj)
        self.db_session.commit()
        self.db_session.refresh(orm_obj)
        logger.info("Strategy has been saved")
        strategy.id = orm_obj.id
        return strategy
