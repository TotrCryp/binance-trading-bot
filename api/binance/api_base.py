import requests
import hmac
import hashlib
from urllib.parse import urlencode
import time
import logging
from core.config import BINANCE_API_KEY, BINANCE_API_SECRET, BINANCE_BASE_URL

logger = logging.getLogger(__name__)


class BaseAPI:
    BASE_URL: str = BINANCE_BASE_URL

    def __init__(self):
        self.api_key = BINANCE_API_KEY
        self.api_secret = BINANCE_API_SECRET.encode()

    def _get_server_timestamp(self) -> int:
        try:
            resp = requests.get(f"{self.BASE_URL}/time", timeout=5)
            resp.raise_for_status()
            data = resp.json()
            return data["serverTime"]
        except Exception as e:
            logger.warning(f"Failed to get server time, falling back to local time: {e}")
            return int(time.time() * 1000)

    def _sign_params(self, params: dict) -> dict:
        query_string = urlencode(params)
        signature = hmac.new(self.api_secret, query_string.encode(), hashlib.sha256).hexdigest()
        params["signature"] = signature
        return params

    def _get_headers(self) -> dict:
        return {"X-MBX-APIKEY": self.api_key}

    @staticmethod
    def prepare_params(params: dict) -> dict:
        result = {}
        for k, v in params.items():
            if isinstance(v, bool):
                v = "true" if v else "false"
            elif isinstance(v, float):
                v = format(v, ".8f").rstrip("0").rstrip(".")
            result[k] = v
        return result

