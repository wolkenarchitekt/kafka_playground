import logging
import re
import time

import click

from website_monitor.kafka_producer import produce
from website_monitor.website_monitor import check_website

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
    while True:
        check_result = check_website(url, match_regex)
        produce(
            timestamp=check_result.timestamp,
            status_code=check_result.status_code,
            matches_regex=check_result.match_regex,
            response_time_seconds=check_result.response_time_seconds,
        )
        time.sleep(sleep_seconds)


if __name__ == "__main__":
    cli()
