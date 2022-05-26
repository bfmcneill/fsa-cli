import pytest
from fsa import utils
from fsa import exceptions


@pytest.fixture()
def good_email():
    return "email@email.com"


@pytest.fixture()
def bad_email():
    return "email.com"


def test_email_validator_success(good_email):
    actual = utils.validate_email(good_email)
    assert actual
    assert isinstance(actual, bool)


def test_email_validator_raises_validation_error(bad_email):
    with pytest.raises(exceptions.ValidatorException) as excinfo:
        utils.validate_email(bad_email)
    assert str(excinfo.value) == "invalid email format"
