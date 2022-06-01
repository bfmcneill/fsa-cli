import pytest

from fsa.models.deposit_service import CheckingAccount
from fsa.exceptions import DepositServiceException


def test_customer_can_create_checking_account(reset_data, customer_with_address):
    email = customer_with_address.email
    checking = CheckingAccount.create(email)
    assert isinstance(checking, CheckingAccount)
    assert checking.owner.email == customer_with_address.email


def test_customer_can_make_initial_checking_deposit(
    reset_data,
    checking_account_with_zero_balance,
):
    checking = checking_account_with_zero_balance
    assert checking.ledger.balance == 0
    checking.deposit(amount=100, memo="initial deposit")
    assert checking.ledger.balance == 100


def test_customer_can_withdraw_from_checking(
    reset_data,
    checking_account_with_1300_balance,
):
    checking = checking_account_with_1300_balance
    assert checking.ledger.balance == 1300
    checking.withdraw(300, memo="taxes")
    assert checking.ledger.balance == 1000


def test_checking_overdraft_attempt_thwarted(
    reset_data,
    checking_account_with_1300_balance,
):
    checking = checking_account_with_1300_balance
    assert checking.ledger.balance == 1300
    with pytest.raises(DepositServiceException):
        checking.withdraw(2000, memo="taxes")


def test_checking_account_ledger_can_export_to_csv(
    reset_data,
    checking_account_with_1300_balance,
    csv_export_dir,
):
    data_dir = csv_export_dir["data_dir"]
    stem = csv_export_dir["stem"]

    checking = checking_account_with_1300_balance
    assert not (data_dir / f"{stem}.csv").exists()
    checking.ledger.to_csv(data_dir, stem=stem)
    assert (data_dir / f"{stem}.csv").exists()
