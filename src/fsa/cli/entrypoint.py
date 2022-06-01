import logging
import click
from fsa.cli.commands import account
from fsa.cli.commands import customer
from fsa.cli.commands import utils

logger = logging.getLogger(__name__)


@click.group()
def cli():
    """cli_tests entrypoint"""


@cli.command()
@click.option("-c", "--case", type=click.Choice(["upper", "lower"]), prompt=True)
def show(case):
    logger.info(f"showing: {case}")
    return "showing"


cli.add_command(account.commands, "account")
cli.add_command(customer.commands, "customer")
cli.add_command(utils.commands, "utils")


if __name__ == "__main__":
    cli()
