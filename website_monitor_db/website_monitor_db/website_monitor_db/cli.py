import logging

import click

from website_monitor_db.website_monitor_db import consume

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
    consume()


if __name__ == "__main__":
    cli()
