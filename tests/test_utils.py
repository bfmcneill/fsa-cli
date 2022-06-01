import pytest
from fsa.utils import email_utils
import email_validator


@pytest.fixture()
def good_email():
    return "stonkmarketape@gmail.com"


@pytest.fixture()
def bad_email():
    return "email.com"


@pytest.fixture()
def bad_email():
    return "email.com"


def test_email_validator_success(good_email):
    actual = email_utils.validate_email(good_email)

    assert actual == good_email


def test_email_validator_raises_validation_error(bad_email):
    with pytest.raises(email_validator.EmailNotValidError) as excinfo:
        email_utils.validate_email(bad_email)

    assert (
        str(excinfo.value)
        == "The email address is not valid. It must have exactly one @-sign."
    )
