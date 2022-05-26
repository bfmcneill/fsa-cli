from email import utils as email_utils
from fsa import exceptions


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
    _, email = email_utils.parseaddr(email)

    if "@" not in email:
        raise exceptions.ValidatorException("invalid email format")

    return True
