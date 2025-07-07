import requests


class BaseAPIClient:
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}

    def get(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        return self._handle_response(response)

    def post(self, endpoint, data=None, json=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, headers=self.headers, data=data, json=json)
        return self._handle_response(response)

    @staticmethod
    def _handle_response(response):
        if response.ok:
            return response.json()
        else:
            # logging.warning('Failed to fetch kline data')
            raise Exception(f"API Error: {response.status_code} - {response.text}")


class CandlestickData(BaseAPIClient):
    def __init__(self):
        super().__init__(base_url="https://api.binance.com")

    def get_kline_data(self, symbol, interval, start_time=0, limit=1000):
        return self.get(f"api/v3/klines", params={'symbol': symbol,
                                                  'interval': interval,
                                                  'startTime': start_time,
                                                  'limit': limit})
