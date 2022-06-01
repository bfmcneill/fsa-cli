import pytest
from click.testing import CliRunner
from fsa.cli import entrypoint

runner = CliRunner()
from fsa.models.customer.customer import Customer


def test_cli_can_create_customer(reset_data):
    """Test that CLI can create customer

    Args(fixtures)
        reset_data  : reset data for test

    """
    email = "jim@gmail.com"
    first_name = "jim"
    last_name = "bo"
    command = [
        "customer",
        "create",
        "--email",
        email,
        "--first-name",
        first_name,
        "--last-name",
        last_name,
    ]
    result = runner.invoke(entrypoint.cli, command)
    _customer = Customer.from_api_using_email(email)
    assert result.exit_code == 0
    assert _customer.id == 1


def test_cli_can_update_customer_having_no_address(
    reset_data: None,
    customer_without_address: Customer,
):
    customer = customer_without_address

    line1 = "8090 Sandstone Court"
    city = "Phoenix"
    state_code = "AZ"
    zip_code = 85331

    command = [
        "customer",
        "update-address",
        "--email",
        customer.email,
        "--line1",
        line1,
        # "--line2",
        # line2,
        "--city",
        city,
        "--state-code",
        state_code,
        "--zip-code",
        zip_code,
    ]

    assert customer.address is None
    result = runner.invoke(entrypoint.cli, command)
    assert customer.address is not None
    assert result.exit_code == 0


def test_cli_can_update_customer_having_an_address(
    reset_data: None,
    customer_with_address: Customer,
):
    customer = customer_with_address

    line1 = "8090 Sandstone Court"
    city = "Phoenix"
    state_code = "AZ"
    zip_code = 85331

    command = [
        "customer",
        "update-address",
        "--email",
        customer.email,
        "--line1",
        line1,
        # "--line2",
        # line2,
        "--city",
        city,
        "--state-code",
        state_code,
        "--zip-code",
        zip_code,
    ]

    # sanity checks
    #   customer does have an address before starting test
    #   current address line1 does not match the new  proposed line1
    assert customer.address is not None
    assert customer.address.line1 != line1

    # run command
    result = runner.invoke(entrypoint.cli, command)
    assert customer.address.line1 == line1
    assert result.exit_code == 0


@pytest.mark.skip(reason="not implemented")
def test_cli_can_list_customer_accounts():
    """Test that CLI can list all the different customer's accounts
    # TODO give customer class ability to query account's it owns from rest api
    """
    return False
