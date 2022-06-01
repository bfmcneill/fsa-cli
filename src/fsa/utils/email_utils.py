import logging
from email_validator import validate_email as _validate_email, EmailNotValidError

logger = logging.getLogger(__name__)


def validate_email(email):
    """Check if email is valid format

    Args:
        email (str)

    Returns
        bool

    ---
    Reference:
    https://docs.python.org/3/library/email.utils.html#email.utils.parseaddr
    """
    try:
        return _validate_email(email).email

    except EmailNotValidError as e:
        logger.error(e)
        raise
