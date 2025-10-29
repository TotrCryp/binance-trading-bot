class Sender:
    def __init__(self):
        self.admin_id = 1

    def send_message(self, message, user_id=-1):
        if user_id < 0:
            user_id = self.admin_id
        print(f"Message: '{message}' sent to user {user_id}")
