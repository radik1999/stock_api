import os
from flask import Flask, jsonify
from flask import request
from core import get_pair_price


app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL=f'redis://{os.environ.get("REDIS_HOST")}:{os.environ.get("REDIS_PORT")}',
    result_backend=f'redis://{os.environ.get("REDIS_HOST")}:{os.environ.get("REDIS_PORT")}'
)


@app.route('/')
def price():
    pair_name = request.args.get("pair_name")
    stock_name = request.args.get("stock_name")

    return jsonify(get_pair_price(pair_name=pair_name, stock_name=stock_name))


if __name__ == '__main__':
    app.run(host="0.0.0.0")
