from loguru import logger


class CustomException(Exception):
    """Custom exception"""


class CustomerExeption(CustomException):
    """Customer exception"""


class ValidatorException(CustomException):
    """Validator exception"""


class ApiException(CustomException):
    """API exceptions"""

    def __init__(self, err_message):
        super().__init__(err_message)
        logger.error(err_message)


class DatabaseException(CustomException):
    """DatabaseException"""

    def __init__(self, err_message):
        super().__init__(err_message)
        logger.error(err_message)
