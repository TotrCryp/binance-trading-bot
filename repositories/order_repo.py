from models import OrderORM, OrderFillORM
from core.domain.order import Order
from core.mixins import ORMConvertibleMixin
from sqlalchemy.orm import Session
from core.logger import get_logger

logger = get_logger(__name__)


class OrderRepository(ORMConvertibleMixin):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def order_to_orm(self, order: Order) -> OrderORM:
        orm_obj = self.to_orm(OrderORM, order)

        if hasattr(order, "fills"):
            # orm_obj.deposit_division_strategy = [
            #     part.model_dump() for part in strategy.deposit_division_strategy
            # ]
            orm_obj.fills = [OrderFillORM(**fill) for fill in order.fills]
        return orm_obj

    def save(self, order: Order) -> Order:
        orm_obj = self.order_to_orm(order)
        self.db_session.add(orm_obj)
        self.db_session.commit()
        self.db_session.refresh(orm_obj)
        logger.info("Order has been saved")
        order.id = orm_obj.id
        return order
