import logging
import click
from fsa.models.customer import customer

logger = logging.getLogger(__name__)


@click.group
def commands():
    """customer commands"""


@commands.command
@click.option("--email", required=True)
@click.option("--first-name", required=True)
@click.option("--last-name", required=True)
def create(email, first_name, last_name):
    """Create a new customer record

    Args:
        email (str)         : customer email
        first_name (str)    : first name
        last_name (str)     : last name
    """
    try:
        c = customer.Customer.new_from_cli(
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
    except Exception as e:
        raise click.Abort()

    logger.debug(f"created new customer: {c}")


@commands.command
@click.option("--email", required=True, type=str)
@click.option("--line1", required=True, type=str)
@click.option("--line2", default="", type=str)
@click.option("--city", required=True, type=str)
@click.option("--state-code", required=True, type=str)
@click.option("--zip-code", required=True, type=str)
def update_address(
    email: str,
    line1: str,
    line2: str,
    city: str,
    state_code: str,
    zip_code: str,
):
    """Update / insert customer address

    Args:
        email       : customer email
        line1       : address line 1
        line2       : address line 2
        city        : city
        state_code  : 2 character state code
        zip_code    : 5 character zip code
    """
    # locate customer by email address
    c = customer.Customer.from_api_using_email(email)

    # build address data from cli command args
    address_data = dict(
        line1=line1,
        line2=line2,
        city=city,
        state_code=state_code,
        zip_code=zip_code,
    )

    # set customer address property
    c.address = address_data


if __name__ == "__main__":
    create(
        [
            "--email",
            "jim@bo.com",
            "--first-name",
            "jim",
            "--last-name",
            "bo",
        ]
    )
