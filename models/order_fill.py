from sqlalchemy import String, Integer, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models import Base


class OrderFillORM(Base):
    # noinspection PyPep8Naming,SpellCheckingInspection
    __tablename__ = "orders_fills"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    price: Mapped[float] = mapped_column(Float)
    qty: Mapped[float] = mapped_column(Float)
    commission: Mapped[float] = mapped_column(Float)
    commissionAsset: Mapped[str] = mapped_column(String(10))
    tradeId: Mapped[int] = mapped_column(Integer)

    # noinspection PyUnresolvedReferences
    order: Mapped["OrderORM"] = relationship(back_populates="fills")
