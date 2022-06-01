import pytest

from fsa.models.deposit_service.savings_account import SavingsAccount
from fsa.models.deposit_service.checking_account import CheckingAccount
from fsa.models.lending_service.credit_card import CreditCard
from fsa.models.lending_service.term_loan import TermLoan
from fsa.exceptions import CustomerException


def test_customer_without_address_can_not_open_accounts(
    reset_data,
    customer_without_address,
):
    with pytest.raises(CustomerException):
        CheckingAccount.create(email=customer_without_address.email)


def test_customer_can_create_savings_account(reset_data, customer_with_address):
    savings = SavingsAccount.create(email=customer_with_address.email, rate=0.035)
    assert isinstance(savings, SavingsAccount)
    assert savings.owner.email == customer_with_address.email
    assert savings.rate == 0.035


def test_customer_can_create_credit_card(reset_data, customer_with_address):
    email = customer_with_address.email
    cc = CreditCard.create(
        email=email,
        rate=0.183,
        limit=3_000,
    )
    assert isinstance(cc, CreditCard)
    assert cc.owner.email == customer_with_address.email
    assert cc.rate == 0.183
    assert cc.limit == 3_000


def test_customer_can_create_term_loan(reset_data, customer_with_address):
    email = customer_with_address.email
    tl = TermLoan.create(
        email=email,
        rate=0.045,
        term=36,
        limit=10_000,
    )
    assert isinstance(tl, TermLoan)
    assert tl.owner.email == customer_with_address.email
    assert tl.rate == 0.045
    assert tl.term == 36
    assert tl.limit == 10_000
