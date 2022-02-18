import json
import requests


from websockets.base_websocket import StockWebSocket


class KrakenWebSocket(StockWebSocket):

    name = "kraken"
    url = f"wss://ws.kraken.com"

    def __init__(self):
        super().__init__()
        self.all_pairs = self.get_all_pairs()

    def on_open(self, ws):
        event = {"event": "subscribe", "subscription": {"name": "ticker"}, "pair": self.all_pairs}
        ws.send(json.dumps(event))

    def on_message(self, ws, message):

        if message.startswith('['):
            self._save_pair_price(message)

    def _save_pair_price(self, pair):
        pairs_price = self.redis.get(self.name)
        formatted_pair = self._format_pair(pair)

        if pairs_price:
            pairs = json.loads(pairs_price)
            pairs.update(formatted_pair)
            pairs = json.dumps(pairs)
        else:
            pairs = json.dumps(formatted_pair)

        self.redis.set(self.name, pairs)

    @staticmethod
    def _format_pair(pair):
        pair = json.loads(pair)
        pair_name = pair[-1]
        pair_price = (float(pair[1]['a'][0]) + float(pair[1]['b'][0])) / 2
        return {pair_name: pair_price}

    @staticmethod
    def get_all_pairs():
        resp = requests.get("https://api.kraken.com/0/public/AssetPairs")

        return [pair["wsname"] for pair in resp.json()["result"].values()]






