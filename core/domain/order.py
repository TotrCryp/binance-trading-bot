from pydantic import BaseModel, Field, ValidationError, field_validator
from typing import List, Optional
from core.logger import get_logger

logger = get_logger(__name__)


class FillSchema(BaseModel):
    price: float
    qty: float
    commission: float
    commissionAsset: str
    tradeId: int


class OrderSchema(BaseModel):
    trading_session_id: int
    symbol: str
    api_orderId: int
    clientOrderId: str
    transactTime: int
    price: float
    origQty: float
    executedQty: float
    origQuoteOrderQty: float
    cummulativeQuoteQty: float
    status: str
    timeInForce: str
    type: str
    side: str
    workingTime: int
    selfTradePreventionMode: Optional[str]
    fills: List[FillSchema] = []

    @field_validator("fills")
    def check_fills_not_empty(cls, v):
        # в майбутьньому можна перевіряти, що список не порожній
        return v


class Fill:
    def __init__(self, price, qty, commission, commissionAsset):
        self.price: float = price
        self.qty: float = qty
        self.commission: float = commission
        self.commissionAsset: str = commissionAsset
        # self.tradeId: int = tradeId


class Order:
    def __init__(self, trading_session_id: int):
        self.trading_session_id = trading_session_id
        self.symbol = "BTCUSDT"
        self.api_orderId = 12345
        self.clientOrderId = "myOrder001"
        self.transactTime = 1725000000000
        self.price = 68000.5
        self.origQty = 0.1
        self.executedQty = 0.1
        self.origQuoteOrderQty = 6800.05
        self.cummulativeQuoteQty = 6800.05
        self.status = "FILLED"
        self.timeInForce = "GTC"
        self.type = "LIMIT"
        self.side = "BUY"
        self.workingTime = 1725000000000
        self.selfTradePreventionMode = None

        self.fills: List[Fill] = []

        one_fill = Fill(price=68000.5, qty=0.1, commission=0.7, commissionAsset="BTC")
        self.fills.append(one_fill)

