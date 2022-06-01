import pytest
from fsa.models.customer.customer import Customer
from fsa.models.customer.address import Address
from fsa.exceptions import CustomerException


def test_create_customer(reset_data):
    data = dict(email="jim@google.com", first_name="jim", last_name="bo")
    c = Customer.new_from_cli(**data)
    assert c.id == 1


def test_duplicate_customer_raises_exception(reset_data):
    c_data1 = dict(email="jim@google.com", first_name="jim", last_name="bo")
    Customer.new_from_cli(**c_data1)
    with pytest.raises(CustomerException):
        Customer.new_from_cli(**c_data1)


def test_null_customer_address_is_none(
    reset_data,
    customer_without_address,
):

    assert customer_without_address.address is None


def test_customer_can_create_address(
    reset_data,
    customer_without_address,
):
    address_data = dict(
        line1="8000 main",
        line2=None,
        city="Phoenix",
        state_code="AZ",
        zip_code=85331,
    )
    customer_without_address.address = address_data
    exists, address = Address.exists(customer_without_address.id)
    assert exists
    assert isinstance(address, Address)


def test_customer_can_change_address(
    reset_data,
    customer_with_address,
):

    address_data = dict(
        line1="300 College Avenue",
        line2="",
        city="Phoenix",
        state_code="AZ",
        zip_code=85331,
    )
    customer_with_address.address = address_data

    exists, address = Address.exists(customer_with_address.id)
    assert exists
    assert isinstance(address, Address)
