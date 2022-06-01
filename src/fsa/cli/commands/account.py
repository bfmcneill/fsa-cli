import click
import logging
from fsa.cli import validators as validator
from fsa.models.deposit_service import checking_account
from fsa.models.deposit_service import savings_account
from fsa.models.lending_service import credit_card
from fsa.models.lending_service import term_loan
from fsa.models.deposit_service import deposit_service
from fsa.exceptions import DepositServiceException

logger = logging.getLogger(__name__)


@click.group
def commands():
    """Account commands"""


@commands.command
@click.option("--email", required=True, type=str, callback=validator.email_validator)
def create_checking(email: str):
    """Create a new checking account

    Args:
        email   : customer email to link the account to
    """
    checking_account.CheckingAccount.create(email)


@commands.command
@click.option("--email", required=True, type=str, callback=validator.email_validator)
@click.option(
    "--rate", required=True, type=float, callback=validator.interest_rate_validator
)
def create_savings(email: str, rate: float):
    """Create a new savings account

    Args:
        email   : customer email to link the account to
        rate    : savings account interest rate between 0 and 1
    """
    savings_account.SavingsAccount.create(email, rate)


@commands.command
@click.option(
    "--email",
    required=True,
    type=str,
    callback=validator.email_validator,
)
@click.option(
    "--rate",
    required=True,
    type=float,
    callback=validator.interest_rate_validator,
)
def create_credit_card(email: str, rate: float):
    """Create a new credit card account

    Args:
        email   : customer email to link the account to
        rate    : credit card annual percentage rate between 0 and 1
    """
    credit_card.CreditCard.create(email, rate)


@commands.command
@click.option(
    "--email",
    required=True,
    type=str,
    callback=validator.email_validator,
)
@click.option(
    "--rate",
    required=True,
    type=float,
    callback=validator.interest_rate_validator,
)
@click.option(
    "--term",
    required=True,
    type=int,
    callback=validator.loan_term_validator,
    help="loan term duration between 12 and 72 months",
)
def create_term_loan(email: str, rate: float, term: int):
    """Create a new term loan

    Args:
        email   : customer email to link the account to
        rate    : credit card annual percentage rate between 0 and 1
        term    : loan term duration between 12 and 72 months
    """
    term_loan.TermLoan.create(email=email, rate=rate, term=term)


@commands.command
@click.option("--account-id", type=int, required=True)
@click.option("--amount", type=float, required=True)
@click.option("--memo", type=str, default="")
def deposit(account_id, amount, memo):
    """Find account by id and deposit"""
    try:
        account = deposit_service.DepositService.from_account_id(account_id)
    except DepositServiceException as e:
        logger.warning(e)
        raise click.Abort()
    except Exception as e:
        logger.error(e)
        raise click.Abort()

    account.deposit(amount, memo)


@commands.command
@click.option("--account-id", type=int, required=True)
@click.option("--amount", type=float, required=True)
@click.option("--memo", type=str, default="")
def withdraw(account_id, amount, memo):
    """Find account by id and withdraw"""
    try:
        account = deposit_service.DepositService.from_account_id(account_id)
        account.withdraw(amount, memo)
    except DepositServiceException as e:
        logger.warning(e)
        raise click.Abort()

    except Exception as e:
        logger.error(e)
        raise click.Abort()

    return True
