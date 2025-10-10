from typing import List, Optional
from sqlalchemy import Float, JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models import Base


class TradingStrategyORM(Base):
    # noinspection PyPep8Naming,SpellCheckingInspection
    __tablename__ = "trading_strategies"

    deposit_division_strategy: Mapped[List] = mapped_column(JSON)
    percentage_min_profit: Mapped[float] = mapped_column(Float)
    market_indicator_to_buy: Mapped[int] = mapped_column(Integer)
    market_indicator_to_sell: Mapped[int] = mapped_column(Integer)
    candle_multiplier: Mapped[int] = mapped_column(Integer)
    # noinspection PyUnresolvedReferences
    trading_session: Mapped[Optional["TradingSessionORM"]] = relationship(
        back_populates="trading_strategy")
