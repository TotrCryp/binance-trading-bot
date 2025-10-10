from sqlalchemy import String, Integer, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models import Base
from typing import List, Optional


class OrderORM(Base):
    # noinspection PyPep8Naming,SpellCheckingInspection
    __tablename__ = "orders"

    trading_session_id: Mapped[int] = mapped_column(ForeignKey("trading_sessions.id"))
    symbol: Mapped[str] = mapped_column(String(10))
    api_orderId: Mapped[int] = mapped_column(Integer)
    orderListId: Mapped[int] = mapped_column(Integer, default=-1)  # Unless it's part of an order list, value will be -1
    clientOrderId: Mapped[str] = mapped_column(String(100))
    transactTime: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Float)
    origQty: Mapped[float] = mapped_column(Float)
    executedQty: Mapped[float] = mapped_column(Float)
    origQuoteOrderQty: Mapped[float] = mapped_column(Float)
    cummulativeQuoteQty: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(50))
    timeInForce: Mapped[str] = mapped_column(String(10))
    type: Mapped[str] = mapped_column(String(50))
    side: Mapped[str] = mapped_column(String(10))
    workingTime: Mapped[int] = mapped_column(Integer)
    selfTradePreventionMode: Mapped[Optional[str]] = mapped_column(String(100))

    # noinspection PyUnresolvedReferences
    fills: Mapped[List["OrderFillORM"]] = relationship(back_populates="order", cascade="all, delete-orphan")
    # noinspection PyUnresolvedReferences
    trading_session: Mapped["TradingSessionORM"] = relationship(back_populates="orders")
