import requests
import logging
from api.binance import BaseAPI

logger = logging.getLogger(__name__)


class BinanceExchangeInfoAPI(BaseAPI):

    def get_exchange_info(self, symbol: str) -> dict:
        params = {"symbol": symbol}
        url = f"{self.BASE_URL}/exchangeInfo"

        try:
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()

            try:
                return resp.json()
            except ValueError as e:
                logger.error(f"Invalid JSON in Binance API response: {e}")
                raise RuntimeError("Failed to parse Binance response as JSON") from e

        except requests.exceptions.Timeout:
            logger.error("Request to Binance API timed out.")
            raise RuntimeError("Binance API request timed out")

        except requests.exceptions.HTTPError as e:
            logger.error(f"Binance API returned HTTP error: {e.response.status_code} {e.response.text}")
            raise RuntimeError(f"Binance API error: {e.response.status_code}")

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error while connecting to Binance: {e}")
            raise RuntimeError("Network error while connecting to Binance") from e