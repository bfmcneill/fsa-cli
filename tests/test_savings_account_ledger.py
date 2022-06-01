import pytest

from fsa.models.deposit_service import SavingsAccount
from fsa.exceptions import DepositServiceException


def test_customer_can_create_savings_account(reset_data, customer_with_address):
    email = customer_with_address.email
    savings = SavingsAccount.create(email, rate=0.075)
    assert isinstance(savings, SavingsAccount)
    assert savings.owner.email == customer_with_address.email


def test_savings_deposit(
    reset_data,
    savings_account_with_zero_balance,
):
    savings = savings_account_with_zero_balance
    assert savings.ledger.balance == 0
    savings.deposit(amount=100, memo="initial deposit")
    assert savings.ledger.balance == 100


def test_savings_withdraw(
    reset_data,
    savings_account_with_1300_balance,
):
    savings = savings_account_with_1300_balance
    assert savings.ledger.balance == 1300
    savings.withdraw(300, memo="taxes")
    assert savings.ledger.balance == 1000


def test_savings_overdraft_error(
    reset_data,
    savings_account_with_1300_balance,
):
    savings = savings_account_with_1300_balance
    assert savings.ledger.balance == 1300
    with pytest.raises(DepositServiceException):
        savings.withdraw(2000, memo="taxes")


def test_savings_account_ledger_can_export_to_csv(
    reset_data,
    savings_account_with_1300_balance,
    csv_export_dir,
):
    data_dir = csv_export_dir["data_dir"]
    stem = csv_export_dir["stem"]

    savings = savings_account_with_1300_balance
    assert not (data_dir / f"{stem}.csv").exists()
    savings.ledger.to_csv(data_dir, stem=stem)
    assert (data_dir / f"{stem}.csv").exists()
