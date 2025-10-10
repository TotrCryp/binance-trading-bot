from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Float, DateTime, func, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models import Base


class TradingSessionORM(Base):
    # noinspection PyPep8Naming,SpellCheckingInspection
    __tablename__ = "trading_sessions"

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    strategy: Mapped[int] = mapped_column(ForeignKey("trading_strategies.id"))
    symbol: Mapped[str] = mapped_column(String(10))
    start_base_amount: Mapped[float] = mapped_column(Float)
    start_quote_amount: Mapped[float] = mapped_column(Float)
    stage: Mapped[int] = mapped_column(Integer)
    average_cost_acquired_assets: Mapped[float] = mapped_column(Float)
    last_action: Mapped[str] = mapped_column(String(10))

    # noinspection PyUnresolvedReferences
    orders: Mapped[List["OrderORM"]] = relationship(back_populates="trading_session", cascade="all, delete-orphan")
    # noinspection PyUnresolvedReferences
    trading_strategy: Mapped["TradingStrategyORM"] = relationship(back_populates="trading_session")
