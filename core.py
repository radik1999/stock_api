import json

from redis.client import Redis

from websockets.binance_websocket import BinanceWebSocket
from websockets.kraken_websocket import KrakenWebSocket


def get_pair_price(pair_name=None, stock_name=None):
    if not stock_name:
        binance_pairs = get_pair_price_in_stock(pair_name)
        kraken_pairs = get_pair_price_in_stock(pair_name, "kraken")

        if not pair_name:
            same_pairs = set(binance_pairs or {}) & set(kraken_pairs or {})
            binance_pairs = {pair_name: binance_pairs[pair_name] for pair_name in same_pairs}
            kraken_pairs = {pair_name: kraken_pairs[pair_name] for pair_name in same_pairs}

        return {
            "binance": binance_pairs,
            "kraken": kraken_pairs
        }

    return {stock_name: get_pair_price_in_stock(pair_name, stock_name)}


def get_pair_price_in_stock(pair_name=None, stock_name="binance"):
    redis_client = Redis(host="redis", port=6379)

    if stock_name == "binance":
        pairs_price = redis_client.get(BinanceWebSocket.name)
    elif stock_name == "kraken":
        pairs_price = redis_client.get(KrakenWebSocket.name)
    else:
        raise Exception("There is no such stock info")

    if not pairs_price:
        return

    pairs_price = json.loads(pairs_price)
    if pair_name:
        if pair_name in pairs_price:
            return {pair_name: pairs_price[pair_name]}
        else:
            return

    return pairs_price
