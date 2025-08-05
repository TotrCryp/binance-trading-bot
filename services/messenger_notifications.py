from services.utils import get_utc_from_timestamp


class Notifier:
    def __init__(self, service):
        self.service = service

    def notify(self, notification):
        self.service.send_message(notification)

    def send_strategy_testing_results(self, top_results):
        text = f"Тестування завершено - результати відсутні" if not top_results \
            else f"Тестування для {top_results[0][0]} завершено:\n"
        for result in top_results:
            utc_start_time = str(get_utc_from_timestamp(result[1]/1000))
            number_transactions = result[4]
            last_transactions_side = result[5]
            utc_finish_time = str(get_utc_from_timestamp(result[6]/1000))
            percentage_of_profit = result[9]
            deposit_division_strategy = result[10]
            percentage_min_profit = result[11]
            market_indicators_strategy = result[12]
            candle_multiplier = result[13]
            strat_res_str = (f"Стратегія dds: {deposit_division_strategy}, pmp: {percentage_min_profit}, "
                             f"mis: {market_indicators_strategy}, cm: {candle_multiplier}.\n"
                             f"Перша угода: {utc_start_time}, проведено {number_transactions} угод, "
                             f"остання угода: {utc_finish_time} ({last_transactions_side}), "
                             f"прибуток: {percentage_of_profit}%.\n"
                             f"*********\n")
            text += strat_res_str
        self.notify(text)
