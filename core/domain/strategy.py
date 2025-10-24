from core.config import STRAT_FILE_PATH
from core.logger import get_logger
from db.trading_strategy import save, get
import json
from typing import List
from pydantic import BaseModel, ValidationError
from api.telegram.sender import Sender


logger = get_logger(__name__)
ts = Sender()


class DepositPartSchema(BaseModel):
    stage: int
    percentage_of_deposit: int
    price_change: float


class TradingStrategySchema(BaseModel):
    symbol: str
    updated_at: int
    deposit_division_strategy: List[DepositPartSchema]
    percentage_min_profit: float
    market_indicator_to_buy: int
    market_indicator_to_sell: int
    candle_multiplier: int


class DepositPart:
    def __init__(self, stage: int, percentage_of_deposit: int, price_change: float):
        self.stage = stage
        self.percentage_of_deposit = percentage_of_deposit
        self.price_change = price_change


class TradingStrategy:
    def __init__(self):
        self.strategy_id: int = 0
        self.symbol: str
        self.updated_at: int = 0
        self.deposit_division_strategy: List[DepositPart] = []
        self.percentage_min_profit: float
        self.market_indicator_to_buy: int
        self.market_indicator_to_sell: int
        self.candle_multiplier: int
        self.update_strategy(init_update=True)

    def update_strategy(self, init_update=False):
        return self.update_strategy_from_json(init_update)

    def update_strategy_from_json(self, init_update=False):
        file_path = STRAT_FILE_PATH
        try:
            with file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            if init_update:
                ts.send_message(f"Strategy JSON not found: {file_path}")
                raise
            return False

        try:
            validated_strategy = TradingStrategySchema(**data)
        except ValidationError as e:
            if init_update:
                # якщо це початкове завантаження — падаємо з помилкою
                ts.send_message(f"Invalid strategy JSON:\n{e}")
                raise ValueError(f"Invalid strategy JSON:\n{e}")
            else:
                # якщо це не перше завантаження — просто логуємо й пропускаємо оновлення
                logger.warning("Strategy validation failed, update skipped", exc_info=e)
                return False

        if validated_strategy.updated_at <= self.updated_at:
            return False

        for key, value in validated_strategy.model_dump().items():
            setattr(self, key, value)

        for key, value in validated_strategy.model_dump().items():
            if key != "deposit_division_strategy":
                setattr(self, key, value)
        self.deposit_division_strategy = [
            DepositPart(**part.model_dump()) for part in validated_strategy.deposit_division_strategy
        ]

        logger.info("Strategy has been updated")
        self.save()
        logger.info("Strategy has been saved")
        return True

    def save(self):
        strategy_id = save(self)
        self.strategy_id = strategy_id

    def get(self):
        d = get(self.strategy_id)

        #  потрібно визначити коли ми беремо атрибути ззовні, а коли з БД

        # deposit_parts = [DepositPart(stage, pct, price) for stage, pct, price in deposit_parts_rows]
        #
        # return TradingStrategy(
        #     symbol=row[1],
        #     updated_at=row[2],
        #     deposit_division_strategy=deposit_parts,
        #     percentage_min_profit=row[3],
        #     market_indicator_to_buy=row[4],
        #     market_indicator_to_sell=row[5],
        #     candle_multiplier=row[6]
        # )
