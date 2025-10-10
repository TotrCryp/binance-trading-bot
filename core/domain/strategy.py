from core.config import STRAT_FILE_PATH
from core.logger import get_logger
import json
from pydantic import BaseModel, Field, ValidationError, field_validator
from typing import List


logger = get_logger(__name__)


class DepositPart(BaseModel):
    stage: int = Field()
    percentage_of_deposit: int = Field(ge=1, le=100)
    price_change: float = Field()


class TradingStrategySchema(BaseModel):
    updated_at: int
    deposit_division_strategy: List[DepositPart]
    percentage_min_profit: float
    market_indicator_to_buy: int
    market_indicator_to_sell: int
    candle_multiplier: int = Field(ge=1)

    @field_validator("deposit_division_strategy")
    def check_not_empty(cls, val):
        if not val:
            raise ValueError("deposit_division_strategy cannot be empty")
        return val


class Strategy:
    def __init__(self):
        self.id = None
        self._file_path = STRAT_FILE_PATH
        self._updated_at: int = 0
        self.deposit_division_strategy: list = []
        self.percentage_min_profit: float = 0.0
        self.market_indicator_to_buy: int = 0
        self.market_indicator_to_sell: int = 0
        self.candle_multiplier: int = 0
        self.update_strategy(True)

    def update_strategy(self, init_update=False):
        file_path = self._file_path
        if not file_path.exists():
            if init_update:
                raise FileNotFoundError(f"Strategy JSON not found: {file_path}")
            else:
                return False

        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
            try:
                validated_strategy = TradingStrategySchema(**data)
            except ValidationError as e:
                if init_update:
                    # якщо це початкове завантаження — падаємо з помилкою
                    raise ValueError(f"Invalid strategy JSON:\n{e}")
                else:
                    # якщо це не перше завантаження — просто логуємо й пропускаємо оновлення
                    logger.warning("Strategy validation failed, update skipped", exc_info=e)
                    return False

            if validated_strategy.updated_at <= self._updated_at:
                return False

            self._updated_at = validated_strategy.updated_at
            self.deposit_division_strategy = validated_strategy.deposit_division_strategy
            self.percentage_min_profit = validated_strategy.percentage_min_profit
            self.market_indicator_to_buy = validated_strategy.market_indicator_to_buy
            self.market_indicator_to_sell = validated_strategy.market_indicator_to_sell
            self.candle_multiplier = validated_strategy.candle_multiplier
            logger.info("Strategy has been updated")
            return True
