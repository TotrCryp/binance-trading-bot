import datetime

from services.utils import (BathDivider,
                            scale_to_range,
                            percentage_difference)


class Tester:
    def __init__(self, candle_dao, symbol, deposit_division_strategy, percentage_min_profit, market_indicators_strategy):
        self._candle_dao = candle_dao
        self._symbol = symbol
        self._start_time = 0
        self._start_base_amount = 1000.00
        self._start_quote_amount = 0.00
        self._number_transactions = 0
        self._last_transactions_side = "start"
        self._finish_time = 0
        self._finish_base_amount = 0.00
        self._finish_quote_amount = 0.00
        self._percentage_of_profit = 0.00
        self._deposit_division_strategy = deposit_division_strategy
        self._percentage_min_profit = percentage_min_profit
        self._market_indicators_strategy = market_indicators_strategy

    @staticmethod
    def get_avg_price(current_data):
        return (current_data[2] + current_data[3]) / 2

    def transaction_result_calculation(self, side, price, amount, timestamp):
        self._last_transactions_side = side
        self._number_transactions += 1
        self._finish_time = timestamp
        if self._start_time == 0:
            self._start_time = timestamp
        if side == "buy":
            self._finish_base_amount -= amount
            self._finish_quote_amount += amount / price
        else:  # "sell"
            self._finish_base_amount += amount * price
            self._finish_quote_amount -= amount

    def check_market_conditions(self, current_data, prev_dataset):
        avg_price = self.get_avg_price(current_data)
        high = max(t[2] for t in prev_dataset)
        low = min(t[3] for t in prev_dataset)
        result = scale_to_range(avg_price, low, high)
        # якщо result > 0, то ціна вища за середню (шкала за-замовчуванням від -10 до 10)
        if self._market_indicators_strategy["s_ind"] < result:
            return "sell"
        elif self._market_indicators_strategy["b_ind"] > result:
            return "buy"
        return ""

    def run_test(self):
        list_deposit_division_strategy = [i[0] for i in self._deposit_division_strategy]
        list_percentage_strategy = [i[1] for i in self._deposit_division_strategy]

        divider = BathDivider(self._start_base_amount, list_deposit_division_strategy)
        dataset = self._candle_dao.get_candles()
        cut_index = 24 * 2
        stage = 1
        last_price = 0

        for i in range(cut_index, len(dataset)):
            current_data = dataset[i]
            prev_dataset = dataset[i - cut_index:i]
            market_conditions = self.check_market_conditions(current_data, prev_dataset)
            if market_conditions == 'buy':
                print(f"{current_data[0]} BUY!")
                if stage < len(list_deposit_division_strategy):
                    current_price = self.get_avg_price(current_data)
                    if stage == 1:
                        # just buy
                        current_base_amount = divider.get_batch(stage)

                        self.transaction_result_calculation("buy", current_price, current_base_amount, current_data[0])
                        last_price = current_price
                        # !iterate stage
                    else:
                        threshold_decrease_percentage = list_percentage_strategy[stage-1]
                        difference = percentage_difference(last_price, current_price)
                        if abs(difference) > threshold_decrease_percentage:
                            # buy
                            current_base_amount = divider.get_batch(stage)
                            self.transaction_result_calculation("buy", current_price, current_base_amount, current_data[0])
                            last_price = current_price
                            # !iterate stage

            elif market_conditions == "sell":
                print(f"{current_data[0]} SELL!")
                if stage > 1:
                    # перевіряємо відсоток різниці
                    pass
                    # якщо продали то last_price = current_price
