import requests
from core.logger import get_logger
from core.sender import Sender
from api.binance import BaseAPI

logger = get_logger(__name__)
sender = Sender()


class BinanceAccountAPI(BaseAPI):

    def get_account_info(self) -> dict:
        params = {
            "timestamp": self._get_server_timestamp(),
            "omitZeroBalances": True
        }
        params = self.prepare_params(params)
        signed_params = self._sign_params(params)
        headers = self._get_headers()
        url = f"{self.BASE_URL}/account"

        try:
            resp = requests.get(url, headers=headers, params=signed_params, timeout=10)
            resp.raise_for_status()

            try:
                return resp.json()
            except ValueError as e:
                logger.error(f"Invalid JSON in Binance API response: {e}")
                sender.send_message(f"Invalid JSON in Binance API response: {e}")
                raise RuntimeError("Failed to parse Binance response as JSON") from e

        except requests.exceptions.Timeout:
            logger.error("Request to Binance API timed out.")
            sender.send_message("Request to Binance API timed out.")
            raise RuntimeError("Binance API request timed out")

        except requests.exceptions.HTTPError as e:
            logger.error(f"Binance API returned HTTP error: {e.response.status_code} {e.response.text}")
            sender.send_message(f"Binance API returned HTTP error: {e.response.status_code} {e.response.text}")
            raise RuntimeError(f"Binance API error: {e.response.status_code}")

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error while connecting to Binance: {e}")
            sender.send_message(f"Network error while connecting to Binance: {e}")
            raise RuntimeError("Network error while connecting to Binance") from e
