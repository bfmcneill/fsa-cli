import pytest
from click.testing import CliRunner
from fsa.cli import entrypoint
from fsa.models.customer.customer import Customer
from fsa.models.deposit_service.savings_account import SavingsAccount

runner = CliRunner()


def test_customer_can_create_savings_account(
    reset_data: None,
    customer_with_address: Customer,
):
    """
    creat a customer savings account

    Args (fixtures):
        reset_data              : reset api data
        customer_with_address   : a customer with an address
    """
    customer = customer_with_address
    command = [
        "account",
        "create-savings",
        "--email",
        customer.email,
        "--rate",
        0.385,
    ]
    result = runner.invoke(entrypoint.cli, command)
    assert result.exit_code == 0


def test_savings_account_deposit_creates_ledger_entry(
    reset_data: None,
    savings_account_with_zero_balance: SavingsAccount,
):
    """Test if the CLI can deposit funds into an existing savings account

    Args (fixtures):
        reset_data  : resets the database
        savings_account_with_zero_balance:  a savings account with zero balance
    """
    savings = savings_account_with_zero_balance

    command = [
        "account",
        "deposit",
        "--account-id",
        savings.id,
        "--amount",
        100,
    ]
    # sanity check account has expected balance before test begins
    assert savings.ledger.balance == 0

    # run command
    runner.invoke(entrypoint.cli, command)
    assert savings.ledger.balance == 100


def test_savings_account_withdraw_creates_ledger_entry(
    reset_data: None,
    savings_account_with_1300_balance: SavingsAccount,
):
    """Test that CLI can withdraw funds from a customer savings account

    Args (fixtures)
        reset_data  : reset data for test
        savings_account_with_1300_balance   : a savings account with funds available for withdraw
    """
    savings = savings_account_with_1300_balance

    command = [
        "account",
        "withdraw",
        "--account-id",
        savings.id,
        "--amount",
        1200,
    ]

    # sanity check account has expected balance before test begins
    assert savings.ledger.balance == 1300
    runner.invoke(entrypoint.cli, command)
    assert savings.ledger.balance == 100


@pytest.mark.skip(reason="test not implemented")
def test_savings_account_ledger_can_export_to_csv():
    return False
