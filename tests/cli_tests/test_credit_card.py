import pytest
from click.testing import CliRunner
from fsa.cli import entrypoint

runner = CliRunner()
from fsa.models.customer.customer import Customer
from fsa.models.lending_service.credit_card import CreditCard


@pytest.mark.skip(reason="not implemented")
def test_cli_can_create_credit_card(
    reset_data: None,
    customer_with_address: Customer,
):
    command = []
    # run command
    result = runner.invoke(entrypoint.cli, command)
    return False


@pytest.mark.skip(reason="not implemented")
def test_cli_can_apply_credit_card_payment(
    reset_data: None,
    credit_card_with_2000_balance_and_3000_limit: CreditCard,
):
    command = []
    # run command
    result = runner.invoke(entrypoint.cli, command)
    return False


@pytest.mark.skip(reason="not implemented")
def test_cli_can_apply_credit_card_disbursement(
    reset_data: None,
    credit_card_with_zero_balance_and_3000_limit: CreditCard,
):
    command = []
    # run command
    result = runner.invoke(entrypoint.cli, command)
    return False


@pytest.mark.skip(reason="not implemented")
def test_cli_can_not_disburse_more_than_credit_card_limit_allows(
    reset_data: None,
    credit_card_with_zero_balance_and_3000_limit: CreditCard,
):
    command = []
    # run command
    result = runner.invoke(entrypoint.cli, command)
    return False


@pytest.mark.skip(reason="not implemented")
def test_cli_will_not_allow_credit_card_overpayment(
    reset_data: None,
    credit_card_with_2000_balance_and_3000_limit: CreditCard,
):
    command = []
    # run command
    result = runner.invoke(entrypoint.cli, command)
    return False
