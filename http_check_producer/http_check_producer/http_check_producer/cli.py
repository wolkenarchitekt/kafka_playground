import logging
import re
import time

import click

from http_check_producer.config import get_config_from_env
from http_check_producer.http_check import http_check
from http_check_producer.producer import HttpCheckProducer

logger = logging.getLogger(__name__)


class RegexParamType(click.ParamType):
    name = "regex"

    def convert(self, value, param, ctx):
        return re.compile(value)


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
@click.option("--url", type=str, required=True)
@click.option(
    "--match-regex",
    type=RegexParamType(),
    required=False,
    help="Check if response content contains regex",
)
@click.option("--sleep-seconds", type=int, default=5)
def run(url, match_regex, sleep_seconds):
    config = get_config_from_env()
    while True:
        check_result = http_check(url, match_regex)
        producer = HttpCheckProducer(config=config)
        producer.produce(http_check_result=check_result)
        time.sleep(sleep_seconds)


@cli.command()
@click.option("--url", type=str, required=True)
@click.option(
    "--match-regex",
    type=RegexParamType(),
    required=False,
    help="Check if response content contains regex",
)
def run_once(url, match_regex):
    config = get_config_from_env()
    producer = HttpCheckProducer(config=config)
    check_result = http_check(url, match_regex)
    producer.produce(http_check_result=check_result)


if __name__ == "__main__":
    cli()
