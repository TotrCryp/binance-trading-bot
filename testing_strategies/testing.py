from services.utils import (DepositDivider,
                            scale_to_range,
                            percentage_difference)


class Tester:
    def __init__(self, candle_dao, test_result_dao, symbol, deposit_division_strategy, percentage_min_profit,
                 market_indicators_strategy, candle_multiplier):
        self._candle_dao = candle_dao
        self._test_result_dao = test_result_dao
        self._symbol = symbol
        self._start_time = 0
        self._start_base_amount = 1000.00
        self._start_quote_amount = 0.00
        self._number_transactions = 0
        self._last_transactions_side = "start"
        self._finish_time = 0
        self._finish_base_amount = 1000.00
        self._finish_quote_amount = 0.00
        self._deposit_division_strategy = deposit_division_strategy
        self._percentage_min_profit = percentage_min_profit
        self._market_indicators_strategy = market_indicators_strategy
        self._candle_multiplier = candle_multiplier
        self._transactions = []
        self._average_cost = 0
        self._stage = 0
        self._last_price = 0

    def record_test_result(self, current_price):

        estimate_quote_amount = self._finish_quote_amount * current_price
        estimate_finish_amount = self._finish_base_amount + estimate_quote_amount

        percentage_of_profit = round(percentage_difference(self._start_base_amount, estimate_finish_amount), 2)
        deposit_division_strategy = str(self._deposit_division_strategy)
        percentage_min_profit = str(self._percentage_min_profit)
        market_indicators_strategy = str(self._market_indicators_strategy)
        candle_multiplier = self._candle_multiplier

        record = (self._symbol, self._start_time, self._start_base_amount, self._start_quote_amount,
                  self._number_transactions, self._last_transactions_side, self._finish_time, self._finish_base_amount,
                  self._finish_quote_amount, percentage_of_profit, deposit_division_strategy, percentage_min_profit,
                  market_indicators_strategy, candle_multiplier)

        self._test_result_dao.set_tests_results(record)

    @staticmethod
    def get_avg_price(current_data):
        return (current_data[2] + current_data[3]) / 2

    def update_average_cost(self):
        sum_q_amount = sum(t[0] for t in self._transactions)
        sum_b_amount = sum(t[1] for t in self._transactions)
        self._average_cost = sum_b_amount / sum_q_amount

    def iterate_stage(self):
        if self._stage < len(self._deposit_division_strategy):
            self._stage += 1
        else:
            self._stage = 0

    def transaction_result_calculation(self, side, price, amount, timestamp):
        self._last_transactions_side = side
        self._number_transactions += 1
        self._finish_time = timestamp
        self._last_price = price
        if self._start_time == 0:
            self._start_time = timestamp
        if side == "buy":
            self._finish_base_amount -= amount
            self._finish_quote_amount += amount / price
            self.iterate_stage()
            self._transactions.append((amount / price, amount))
            self.update_average_cost()
        else:  # "sell"
            self._finish_base_amount += amount * price
            self._finish_quote_amount -= amount
            self._stage = 0
            self._transactions = []
            self._average_cost = 0

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

        divider = DepositDivider(self._start_base_amount, list_deposit_division_strategy)
        dataset = self._candle_dao.get_candles()
        cut_index = 24 * self._candle_multiplier

        for i in range(cut_index, len(dataset)):
            current_data = dataset[i]
            prev_dataset = dataset[i - cut_index:i]
            market_conditions = self.check_market_conditions(current_data, prev_dataset)
            if market_conditions == 'buy':
                if self._stage < len(list_deposit_division_strategy):
                    current_price = self.get_avg_price(current_data)
                    if self._stage == 0:
                        current_base_amount = divider.get_batch(self._stage)
                        self.transaction_result_calculation("buy", current_price, current_base_amount, current_data[0])
                        divider.set_remnant(self._finish_base_amount)
                    else:
                        threshold_decrease_percentage = list_percentage_strategy[self._stage]
                        difference = percentage_difference(self._last_price, current_price)
                        if self._last_price > current_price and abs(difference) > threshold_decrease_percentage:
                            current_base_amount = divider.get_batch(self._stage)
                            self.transaction_result_calculation("buy", current_price,
                                                                current_base_amount, current_data[0])
                            divider.set_remnant(self._finish_base_amount)
            elif market_conditions == "sell":
                if self._stage:
                    current_price = self.get_avg_price(current_data)
                    difference = percentage_difference(self._average_cost, current_price)
                    if difference > self._percentage_min_profit:
                        self.transaction_result_calculation("sell", current_price,
                                                            self._finish_quote_amount, current_data[0])
                        divider.set_remnant(self._finish_base_amount)

        current_price = self.get_avg_price(dataset[-1])
        self.record_test_result(current_price)
