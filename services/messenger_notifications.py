class Notifier:
    def __init__(self, service):
        self.service = service

    def notify(self, notification):
        self.service.send_message(notification)
