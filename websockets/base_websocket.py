import os

import websocket
from redis.client import Redis


class StockWebSocket:
    def __init__(self):
        self.redis = Redis(host=os.environ.get("REDIS_HOST"), port=int(os.environ.get("REDIS_PORT")))
        self.ws = websocket.WebSocketApp(
            self.url, on_open=self.on_open, on_message=self.on_message, on_close=self.on_close
        )

    def on_open(self, ws):
        print("### opened ###")

    def on_close(self, ws, close_status_code, close_msg):
        print("### closed ###")

    def on_message(self, ws, message):
        print("### message ###")

    def connect(self):
        if not self.ws.keep_running:
            self.ws.run_forever()

    def disconnect(self):
        if self.ws.keep_running:
            self.ws.close()
