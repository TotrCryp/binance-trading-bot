class Strategist:
    def __init__(self):
        self._min_b_ind = -10
        self._max_s_ind = 10
        self._max_profit = 5
        self._max_profit_step = 0.2

    def get_strategy_set(self):
        list_deposit_division_strategies = [
            [(20, 0), (30, 1), (50, 1)],
            [(20, 0), (30, 2), (50, 3)],
            [(20, 0), (30, 3), (50, 5)],
            [(20, 0), (20, 1), (30, 1), (30, 1)],
            [(20, 0), (20, 1), (30, 2), (30, 3)],
            [(20, 0), (20, 2), (30, 4), (30, 6)],
            [(20, 0), (20, 1), (20, 1), (40, 1)],
            [(20, 0), (20, 1), (20, 2), (40, 3)],
            [(20, 0), (20, 2), (20, 4), (40, 6)],
            [(20, 0), (20, 1), (20, 1), (20, 1), (20, 1)],
            [(20, 0), (20, 1), (20, 2), (20, 3), (20, 4)],
            [(20, 0), (20, 2), (20, 4), (20, 6), (20, 8)]
        ]

        list_market_indicators_strategy = []
        s_ind = 0
        while s_ind <= self._max_s_ind:
            b_ind = 0
            while b_ind >= self._min_b_ind:
                list_market_indicators_strategy.append({"b_ind": b_ind, "s_ind": s_ind})
                b_ind -= 0.5
            s_ind += 0.5

        strategy_set = []

        percentage_min_profit = 0.6
        while percentage_min_profit <= self._max_profit:
            for dds in list_deposit_division_strategies:
                for mis in list_market_indicators_strategy:
                    for cm in range(1, 15):
                        strategy_set.append({"deposit_division_strategy": dds,
                                             "percentage_min_profit": percentage_min_profit,
                                             "market_indicators_strategy": mis,
                                             "candle_multiplier": cm})
            percentage_min_profit += self._max_profit_step

        return strategy_set
