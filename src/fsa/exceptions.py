import logging

logger = logging.getLogger(__name__)


class CustomException(Exception):
    def __init__(self, err_message):
        # logger.debug(err_message)
        super().__init__(err_message)


class CustomerException(CustomException):
    """Customer exception"""


class ValidatorException(CustomException):
    """Validator exception"""


class ApiException(CustomException):
    """API exceptions"""


class DatabaseException(CustomException):
    """Database exception"""


class DepositServiceException(CustomException):
    """Deposit service exception"""


class AccountException(CustomException):
    """Account exception"""


class LedgerExecption(CustomException):
    """Ledger exception"""


class LendingServiceException(CustomException):
    """Lending service exception"""


class AddressException(CustomException):
    """Address exception"""
