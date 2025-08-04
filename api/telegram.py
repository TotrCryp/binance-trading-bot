import requests
import logging


class TelegramAPI:
    def __init__(self, token, owner_chat_id):
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.owner_chat_id = owner_chat_id

    def send_message(self, message, chat_id=None):
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": chat_id if chat_id else self.owner_chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, data=payload)
        if not response.ok:
            logging.warning(
                f"Telegram message failed. Status code: {response.status_code}, "
                f"Text: {response.text}, URL: {url}, Payload: {payload}"
            )
        else:
            logging.info(f"Telegram message has been sent. Status code: {response.status_code}")
