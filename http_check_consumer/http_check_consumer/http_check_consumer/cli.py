import logging

import click

from http_check_consumer.config import (
    get_kafka_config_from_env,
    get_postgres_config_from_env,
)
from http_check_consumer.consumer_to_db import ConsumerToDB

logger = logging.getLogger(__name__)


@click.group()
@click.option("-v", "--verbose", is_flag=True, help="Verbose logging")
@click.option("-d", "--debug", is_flag=True, help="Debug logging")
def cli(verbose, debug):
    loglevel = logging.WARNING
    if verbose:
        loglevel = logging.INFO
    elif debug:
        loglevel = logging.DEBUG
    logging.basicConfig(level=loglevel)


@cli.command()
def run():
    consumer_to_tb = ConsumerToDB(
        kafka_config=get_kafka_config_from_env(),
        postgres_config=get_postgres_config_from_env(),
    )
    consumer_to_tb.consume_messages()


@cli.command()
def run_once():
    consumer_to_tb = ConsumerToDB(
        kafka_config=get_kafka_config_from_env(),
        postgres_config=get_postgres_config_from_env(),
    )
    consumer_to_tb.consume_next_message()


if __name__ == "__main__":
    cli()
