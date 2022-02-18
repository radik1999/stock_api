from flask.cli import FlaskGroup


from app import app
from celery_service import run_binance_task, run_kraken_task

cli = FlaskGroup(app)


@cli.command("run_websockets")
def run_websockets():
    run_binance_task.delay()
    # run_kraken_task.delay()


if __name__ == "__main__":
    cli()
