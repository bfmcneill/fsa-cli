import pytest
from fsa.models.customer.customer import Customer
from fsa.models.lending_service.term_loan import TermLoan
from fsa.models.lending_service.credit_card import CreditCard
from fsa.utils import api_utils
from fsa.models.deposit_service.checking_account import CheckingAccount
from fsa.models.deposit_service.savings_account import SavingsAccount
from fsa.settings import data_dir


@pytest.fixture()
def reset_data():
    """Reset api data collections
    There are two ways to do this, one is through api DELETE requests
    and the other way is to just overwrite the json file (database)
    with desired initial state.
    """
    # api_utils.delete_collection("customers")
    # api_utils.delete_collection("accounts")
    # api_utils.delete_collection("ledger")
    # api_utils.delete_collection("addresses")
    api_utils.reset_db_json()
    # create a new line before tests run so any logging output is not interleaved
    # https://github.com/pytest-dev/pytest/issues/8574#issuecomment-828756544
    print()


@pytest.fixture()
def csv_export_dir():
    yield dict(data_dir=data_dir, stem="test_output")
    csv_path = data_dir / "test_output.csv"
    csv_path.unlink()


@pytest.fixture()
def customer_with_address():
    """Create a customer with an address

    Returns
        Customer
    """
    customer_data = dict(
        email="jim@google.com",
        first_name="jim",
        last_name="bo",
    )
    address_data = dict(
        line1="8000 broadway",
        line2=None,
        city="Phoenix",
        state_code="AZ",
        zip_code="85331",
    )
    customer = Customer.new_from_cli(**customer_data)
    customer.address = address_data
    return customer


@pytest.fixture()
def customer_without_address():
    """Create a customer without an address

    Returns
        Customer
    """
    customer_data = dict(
        email="jim@google.com",
        first_name="jim",
        last_name="bo",
    )

    return Customer.new_from_cli(**customer_data)


@pytest.fixture
def checking_account_with_zero_balance(customer_with_address: Customer):
    email = customer_with_address.email
    return CheckingAccount.create(email)


@pytest.fixture
def checking_account_with_1300_balance(
    customer_with_address: Customer,
    checking_account_with_zero_balance: CheckingAccount,
):
    checking = checking_account_with_zero_balance
    checking.deposit(100, "initial deposit")
    checking.deposit(200, "birthday gift")
    checking.deposit(1050, "initial deposit")
    checking.withdraw(50, "cell phone bill")
    checking.deposit(1000, "w2 salary")
    checking.withdraw(1000, "rent")
    return checking


@pytest.fixture
def savings_account_with_zero_balance(customer_with_address: Customer):
    email = customer_with_address.email
    return SavingsAccount.create(email, rate=0.075)


@pytest.fixture
def savings_account_with_1300_balance(
    customer_with_address,
    savings_account_with_zero_balance: SavingsAccount,
):
    savings = savings_account_with_zero_balance
    savings.deposit(100, "initial deposit")
    savings.deposit(200, "birthday gift")
    savings.deposit(1050, "initial deposit")
    savings.withdraw(50, "cell phone bill")
    savings.deposit(1000, "w2 salary")
    savings.withdraw(1000, "rent")
    return savings


@pytest.fixture()
def credit_card_with_zero_balance_and_3000_limit(
    customer_with_address: Customer,
):

    email = customer_with_address.email
    return CreditCard.create(email, rate=0.18, limit=3_000)


@pytest.fixture()
def credit_card_with_2000_balance_and_3000_limit(
    credit_card_with_zero_balance_and_3000_limit: CreditCard,
):
    cc = credit_card_with_zero_balance_and_3000_limit
    cc.disbursement(amount=2_000, memo="cash advance")
    return cc


@pytest.fixture()
def term_loan_36_months_for_30k(customer_with_address: Customer):
    email = customer_with_address.email
    return TermLoan.create(email, rate=0.045, term=36, limit=30_000)


@pytest.fixture()
def term_loan_36_months_for_30k_with_2_payments_applied(
    term_loan_36_months_for_30k: TermLoan,
):
    tl = term_loan_36_months_for_30k
    tl.payment(2_000)
    tl.payment(2_000)
    return tl
