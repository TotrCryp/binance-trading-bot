

# class Order:
#     def __init__(self, symbol,
#                  start_base_amount,
#                  start_quote_amount,
#                  stage,
#                  average_cost_acquired_assets,
#                  last_action, strategy):
#         self.id: int | None = None
#         b, q = self.split_symbol(symbol)
#         self.symbol: str = b + q
#         self._base_asset: str = b
#         self._quote_asset: str = q
#         self.start_base_amount: float = start_base_amount
#         self.start_quote_amount: float = start_quote_amount
#         self.stage: int = stage
#         self.average_cost_acquired_assets: float = average_cost_acquired_assets
#         self.last_action: str = last_action
#         self.strategy: Strategy = strategy
