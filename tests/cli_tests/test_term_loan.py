import pytest
from click.testing import CliRunner
from fsa.cli import entrypoint

runner = CliRunner()
from fsa.models.customer.customer import Customer
from fsa.models.lending_service.term_loan import TermLoan


@pytest.mark.skip(reason="not implemented")
def test_cli_can_create_term_loan(
    reset_data: None,
    customer_with_address: Customer,
):
    command = []
    # run command
    result = runner.invoke(entrypoint.cli, command)
    return False


@pytest.mark.skip(reason="not implemented")
def test_cli_can_apply_term_loan_payment(
    reset_data: None,
    term_loan_36_months_for_30k: TermLoan,
):
    command = []
    # run command
    result = runner.invoke(entrypoint.cli, command)
    return False


@pytest.mark.skip(reason="not implemented")
def test_cli_will_not_allow_term_loan_disbursement(
    reset_data: None,
    term_loan_36_months_for_30k_with_2_payments_applied: TermLoan,
):
    command = []
    # run command
    result = runner.invoke(entrypoint.cli, command)
    return False


@pytest.mark.skip(reason="not implemented")
def test_cli_will_not_allow_term_loan_overpayment(
    reset_data: None,
    term_loan_36_months_for_30k: TermLoan,
):
    command = []
    # run command
    result = runner.invoke(entrypoint.cli, command)
    return False
