import pytest
from click.testing import CliRunner
from fsa.cli import entrypoint
from fsa.models.customer.customer import Customer
from fsa.models.deposit_service.checking_account import CheckingAccount

runner = CliRunner()


def test_customer_can_create_checking_account(
    reset_data: None,
    customer_with_address: Customer,
):
    """
    creat a customer checking account

    Args (fixtures):
        reset_data              : reset api data
        customer_with_address   : a customer with an address
    """
    customer = customer_with_address
    command = [
        "account",
        "create-checking",
        "--email",
        customer.email,
    ]
    result = runner.invoke(entrypoint.cli, command)
    assert result.exit_code == 0


def test_checking_account_deposit_creates_ledger_entry(
    reset_data: None,
    checking_account_with_zero_balance: CheckingAccount,
):
    """Test if the CLI can deposit funds into an existing checking account

    Args (fixtures):
        reset_data  : resets the database
        checking_account_with_zero_balance:  a checking account with zero balance
    """
    checking = checking_account_with_zero_balance

    command = [
        "account",
        "deposit",
        "--account-id",
        checking.id,
        "--amount",
        100,
    ]
    # sanity check account has expected balance before test begins
    assert checking.ledger.balance == 0

    # run command and assert
    runner.invoke(entrypoint.cli, command)
    assert checking.ledger.balance == 100


def test_checking_account_withdraw_creates_ledger_entry(
    reset_data: None,
    checking_account_with_1300_balance: CheckingAccount,
):
    """Test that CLI can withdraw funds from a customer checking account

    Args (fixtures)
        reset_data  : reset data for test
        savings_account_with_1300_balance   : a checking account with funds available for withdraw
    """
    checking = checking_account_with_1300_balance

    command = [
        "account",
        "withdraw",
        "--account-id",
        checking.id,
        "--amount",
        1200,
    ]

    # sanity check account has expected balance before test begins
    assert checking.ledger.balance == 1300

    # run command
    runner.invoke(entrypoint.cli, command)
    assert checking.ledger.balance == 100


@pytest.mark.skip(reason="test not implemented")
def test_checking_account_ledger_can_export_to_csv():
    return False
