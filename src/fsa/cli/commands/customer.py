import click
from fsa.models import customer
from fsa.models import account_type as account_type_enum
from fsa.models import account
from loguru import logger
from fsa import utils, exceptions


def validate_email(ctx, param, value):
    try:
        utils.validate_email(value)
        return value
    except exceptions.ValidatorException as e:
        raise click.BadParameter(e)
    except Exception as e:
        logger.error(e)
        raise


@click.group
def commands():
    """customer commands"""


@commands.command
@click.option("--email", required=True)
@click.option("--first-name", required=True)
@click.option("--last-name", required=True)
def create_profile(email, first_name, last_name):
    """
    TODO: simplify error handling so there is not so many try / except blocks
    """
    try:
        c = customer.Customer.from_cli(
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        logger.debug(f"created: {c}")
    except Exception as e:
        logger.error("error creating profile")


@commands.command()
@click.option(
    "--account-type",
    required=True,
    type=click.Choice(account_type_enum.AccountType.__members__),
)
@click.option(
    "--email",
    callback=validate_email,
    required=True,
)
def create_account(account_type, email):
    logger.debug(f"creating account: {account_type}")
    account.Account.from_customer_email(email=email, account_type=account_type)


@commands.command()
@click.option(
    "--email",
    # callback=utils.validate_email,
    required=True,
)
def find_by_email(email):
    customer.Customer.from_email(email=email)
