class Notifier:
    def __init__(self, service):
        self.service = service

    def notify(self, notification):
        self.service.send_message(notification)

    def send_strategy_testing_results(self, top_results):
        text = f"Тестування завершено - результати відсутні" if not top_results \
            else f"Тестування для {top_results[0][0]} завершено:\n"
        for result in top_results:
            text += "test"
        self.notify(text)
