import pytest

from fsa.models.lending_service.term_loan import TermLoan
from fsa.exceptions import LendingServiceException


def test_customer_can_create_term_loan(reset_data, customer_with_address):
    email = customer_with_address.email
    tl = TermLoan.create(email, rate=0.125, limit=3_000, term=36)
    assert isinstance(tl, TermLoan)
    assert tl.owner.email == customer_with_address.email
    assert tl.ledger.balance == 3_000


def test_customer_can_make_term_loan_payment(
    reset_data,
    term_loan_36_months_for_30k,
):
    tl = term_loan_36_months_for_30k
    assert tl.ledger.balance == 30_000
    tl.payment(2_000, memo="first payment")
    assert tl.ledger.balance == 28_000


def test_term_loan_does_not_have_disburse_action_after_funding(
    reset_data,
    term_loan_36_months_for_30k,
):
    tl = term_loan_36_months_for_30k
    assert tl.ledger.balance == 30_000
    tl.payment(
        2_000,
        "first payment should reduce balance enough to make room for another disbursement...right?",
    )
    with pytest.raises(LendingServiceException):
        tl.disbursement(100, memo="hehe nice try buddy")


def test_credit_card_ledger_can_export_to_csv(
    reset_data,
    term_loan_36_months_for_30k_with_2_payments_applied,
    csv_export_dir,
):
    data_dir = csv_export_dir["data_dir"]
    stem = csv_export_dir["stem"]

    tl = term_loan_36_months_for_30k_with_2_payments_applied
    assert not (data_dir / f"{stem}.csv").exists()
    tl.ledger.to_csv(data_dir, stem=stem)
    assert (data_dir / f"{stem}.csv").exists()
