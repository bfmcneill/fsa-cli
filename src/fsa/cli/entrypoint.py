import click
from fsa.cli.commands import account
from fsa.cli.commands import customer


@click.group()
def cli():
    """cli_tests entrypoint"""


cli.add_command(account.commands, "account")
cli.add_command(customer.commands, "customer")


@cli.command()
@click.option("-c", "--case", type=click.Choice(["upper", "lower"]), prompt=True)
def show(case):
    return "showing"


if __name__ == "__main__":
    cli()
