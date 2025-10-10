from core.domain.strategy import Strategy


class TradingSession:
    def __init__(self, symbol,
                 start_base_amount,
                 start_quote_amount,
                 stage,
                 average_cost_acquired_assets,
                 last_action, strategy):
        self.id: int | None = None
        self.symbol: str = symbol
        self.start_base_amount: float = start_base_amount
        self.start_quote_amount: float = start_quote_amount
        self.stage: int = stage
        self.average_cost_acquired_assets: float = average_cost_acquired_assets
        self.last_action: str = last_action
        self.strategy: Strategy = strategy
