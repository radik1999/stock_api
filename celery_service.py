from celery import Celery
from app import app

from websockets.binance_websocket import BinanceWebSocket
from websockets.kraken_websocket import KrakenWebSocket

celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)
periodic_time = 300

binance = BinanceWebSocket()
kraken = KrakenWebSocket()


@celery.task(name="binance")
def run_binance_task():
    binance.connect()


@celery.task(name="kraken")
def run_kraken_task():
    kraken.connect()


celery.conf.beat_schedule = {
    "run_binance": {
        "task": "binance",
        "schedule": periodic_time
    },
    "run_kraken": {
        "task": "kraken",
        "schedule": periodic_time
    }
}
