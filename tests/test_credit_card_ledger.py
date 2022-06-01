import pytest

from fsa.models.lending_service.credit_card import CreditCard
from fsa.exceptions import LendingServiceException


def test_customer_can_create_credit_card(reset_data, customer_with_address):
    email = customer_with_address.email
    cc = CreditCard.create(email, rate=0.125, limit=3_000)
    assert isinstance(cc, CreditCard)
    assert cc.owner.email == customer_with_address.email


def test_customer_can_make_credit_card_advance(
    reset_data,
    credit_card_with_zero_balance_and_3000_limit,
):
    cc = credit_card_with_zero_balance_and_3000_limit
    assert cc.ledger.balance == 0
    cc.disbursement(amount=100, memo="cash advance")
    assert cc.ledger.balance == 100


def test_customer_can_make_credit_card_payment(
    reset_data,
    credit_card_with_2000_balance_and_3000_limit,
):
    cc = credit_card_with_2000_balance_and_3000_limit
    assert cc.ledger.balance == 2_000
    cc.payment(2_000, memo="taxes")
    assert cc.ledger.balance == 0


def test_credit_card_over_limit_attempt_thwarted(
    reset_data,
    credit_card_with_2000_balance_and_3000_limit,
):
    cc = credit_card_with_2000_balance_and_3000_limit
    assert cc.ledger.balance == 2_000
    with pytest.raises(LendingServiceException):
        cc.disbursement(2000, memo="cash advance")


def test_credit_card_ledger_can_export_to_csv(
    reset_data,
    credit_card_with_2000_balance_and_3000_limit,
    csv_export_dir,
):
    data_dir = csv_export_dir["data_dir"]
    stem = csv_export_dir["stem"]

    cc = credit_card_with_2000_balance_and_3000_limit
    assert not (data_dir / f"{stem}.csv").exists()
    cc.ledger.to_csv(data_dir, stem=stem)
    assert (data_dir / f"{stem}.csv").exists()
