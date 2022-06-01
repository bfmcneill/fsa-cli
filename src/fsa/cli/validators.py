import click
from email_validator import validate_email, EmailSyntaxError


def email_validator(ctx, param, value: str) -> str:
    """Validate text representing email address

    Args
        ctx     : click context
        param   : command option --email
        value   : email to be validated

    Returns
        value   : valid email

    Raises
        click.BadParameter when EmailSyntaxError is thrown
    """
    try:
        return validate_email(value).email
    except EmailSyntaxError:
        raise click.BadParameter("invalid email syntax")


def interest_rate_validator(
    ctx: click.core.Context,
    param: click.core.Parameter,
    value: float,
) -> float:
    """Validate interest rate=

    Args
        ctx     : click context
        param   : command option --rate
        value   : interest rate to be validated

    Returns
        value   : valid interest rate

    Raises
        click.BadParameter when value is not numeric or between 0 and 1
    """
    try:
        _rate = float(value)
        if 0 < _rate < 1:
            return _rate
        raise ValueError
    except Exception:
        raise click.BadParameter("rate must be numeric and between 0 and 1")


def loan_term_validator(
    ctx: click.core.Context,
    param: click.core.Parameter,
    value: int,
) -> int:
    """Validate loan term duration

    Args
        ctx     : click context
        param   : command option --rate
        value   : loan term duration

    Returns
        value   : valid loan term duration

    Raises
        click.BadParameter when value is not numeric or between 12 and 72
    """
    try:
        _rate = int(value)
        if 12 < _rate < 72:
            return _rate
        raise ValueError
    except Exception:
        raise click.BadParameter("rate must be numeric and between 12 and 72")
