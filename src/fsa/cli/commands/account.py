import click
from fsa.models import account
from fsa.models import customer
from fsa.models import account_type


@click.group
def commands():
    """Account commands"""


@commands.command
@click.option("--email")
@click.option("--account-type", type=account_type.AccountType)
def create(email, account_type):
    """Create a new account

    Args:
        email (str): customer email to link the account to
    """
    c = customer.Customer.from_email(email)
    a = account.Account._http_create(customer=c, account_type=account_type)
