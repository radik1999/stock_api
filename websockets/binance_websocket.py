import json
import requests


from websockets.base_websocket import StockWebSocket


class BinanceWebSocket(StockWebSocket):

    name = "binance"
    url = f"wss://stream.binance.com:9443/ws/!ticker@arr"

    def __init__(self):
        super().__init__()
        self.all_pairs = self._get_all_pairs()

    def on_message(self, ws, message):
        self._save_pairs_price(message)

    def _save_pairs_price(self, pairs_ticker):
        pairs_ticker = json.loads(pairs_ticker)
        formatted_pairs = dict(map(self._format_pair, pairs_ticker))

        old_pairs = self.redis.get(self.name)
        if old_pairs:
            pairs = json.loads(old_pairs)
            pairs.update(formatted_pairs)
        else:
            pairs = formatted_pairs

        self.redis.set(self.name, json.dumps(pairs))

    def _format_pair(self, pair_ticker):
        pair_name = self.all_pairs[pair_ticker['s']]
        pair_price = (float(pair_ticker['b']) + float(pair_ticker['a'])) / 2
        return pair_name, pair_price

    @staticmethod
    def _get_all_pairs():
        resp = requests.get("https://api.binance.com/api/v3/exchangeInfo")
        return {
            pair["symbol"]: "/".join((pair["baseAsset"], pair["quoteAsset"]))
            for pair in resp.json()["symbols"]
        }
