from typing import Union
import requests
from loguru import logger
from fsa import exceptions
from fsa import settings


class Customer:
    def __init__(
        self,
        customer_id: int,
        email: str,
        first_name: str,
        last_name: str,
        **kwargs,
    ) -> None:
        self.customer_id = customer_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return f"<Customer id={self.customer_id}, email={self.email}>"

    @classmethod
    def from_id(cls, **kwargs):
        """Create customer from database using customer id lookup

        Args:
            customer_id (int)

        return Customer
        """
        try:
            customer_id = kwargs["customer_id"]
            url = f"{settings.BASE_URL}/customers/{customer_id}"
            r = requests.get(url, params=dict(**kwargs))
            data = r.json()[0]
            return Customer(**data)

        except requests.exceptions.ConnectionError:
            exceptions.ApiException(f"{settings.BASE_URL} is not responding")

        except IndexError as e:
            raise exceptions.DatabaseException("customer id not found")

        except Exception as e:
            logger.error(e)
            raise

    @classmethod
    def from_email(cls, **kwargs):
        """Create customer from database using email lookup

        Args:
            email (str)

        return Customer
        """

        try:
            url = f"{settings.BASE_URL}/customers"
            r = requests.get(url, params=dict(**kwargs))
            data = r.json()[0]
            c = Customer(customer_id=data["id"], **data)
            return c

        except requests.exceptions.ConnectionError:
            raise exceptions.ApiException(f"{settings.BASE_URL} is not responding")

        except IndexError as e:
            exceptions.DatabaseException("customer email not found")
            return None

        except Exception as e:
            logger.error(e)
            raise

    @classmethod
    def from_cli(cls, *args, **kwargs):
        """Create customer from CLI input

        Args
            email (str)
            first_name (str)
            last_name (str)

        returns
            Union[Customer,None]
        """
        # TODO: if request is success but a separate error is raised the transaction needs roll back
        try:

            # check if customer already exists, lookup customer by email
            c = Customer.from_email(email=kwargs["email"])
            if c:
                raise exceptions.CustomerExeption("customer already exists")
                return None

            payload = dict(**kwargs)
            url = f"{settings.BASE_URL}/customers"
            r = requests.post(url, data=payload)
            customer_id = r.json()["id"]
            return Customer(customer_id=customer_id, **kwargs)

        except requests.exceptions.ConnectionError:
            raise exceptions.ApiException(f"{settings.BASE_URL} is not responding")

        except IndexError as e:
            raise exceptions.DatabaseException("customer email not found")

        except Exception as e:
            logger.error(e)
            raise
