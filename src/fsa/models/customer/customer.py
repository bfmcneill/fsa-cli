import requests
import logging
from fsa import exceptions
from fsa import settings
from fsa.models.customer.address import Address
from fsa.utils import email_utils
from fsa.utils.request_utils import requests_retry_session

logger = logging.getLogger(__name__)


class Customer:
    rest_endpoint = f"{settings.BASE_URL}/customers"

    def __init__(
        self,
        id: int,
        email: str,
        first_name: str,
        last_name: str,
    ):
        self.id = id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    @property
    def address(self) -> Address:

        logger.debug("find address from customer id")
        exists, address = Address.exists(customer_id=self.id)

        if exists:
            return address

        logger.debug("customer address not found")
        return None

    @address.setter
    def address(self, data):
        """set the customer address

        Args:
            data (dict) : address data, keys line1,line2,city,state_code,zip_code
        """
        # validate that data contains all required keys
        required_keys = ["line1", "line2", "city", "state_code", "zip_code"]
        for k in required_keys:
            if k not in data.keys():
                raise exceptions.CustomerException(f"address requires {k}")

        Address.upsert(customer_id=self.id, data=data)

    def __repr__(self):
        return f"{__class__.__name__}(id={self.id}, email={self.email}, fist_name={self.first_name}, last_name={self.last_name})"

    @classmethod
    def email_exists(cls, email: str) -> bool:
        """Query the api to see if an email exists

        Args:
            email (str): email to lookup

        Returns:
            bool
        """

        if not email_utils.validate_email(email):
            err_msg = f"{email} is not a valid email format"
            raise exceptions.CustomerException(err_msg)

        params = dict(email=email)
        r = requests_retry_session().get(cls.rest_endpoint, params=params)

        if not r.ok:
            err_msg = f"API error: GET {cls.rest_endpoint} resulted in {r.status_code}"
            raise exceptions.ApiException(err_msg)

        return len(r.json()) == 1

    @classmethod
    def from_id(cls, id):
        """Create instance from api using customer id

        Args:
            id (int)

        return Customer
        """
        try:
            url = f"{cls.rest_endpoint}/{id}"
            r = requests_retry_session().get(url)
            data = r.json()
            return cls(
                id=data["id"],
                email=data["email"],
                first_name=data["first_name"],
                last_name=data["last_name"],
            )

        except requests.exceptions.ConnectionError:
            exceptions.ApiException("server is not responding")

        except IndexError as e:
            raise exceptions.DatabaseException("customer not found")

        except Exception as e:
            logger.error(e)
            raise

    @classmethod
    def from_api_using_email(cls, email):
        """Create customer instance using data supplied from API

        Args:
            email (str)

        return Customer
        """
        params = dict(email=email)
        r = requests_retry_session().get(cls.rest_endpoint, params=params)

        if not r.ok:
            err_msg = f"API error: GET {cls.rest_endpoint} resulted in {r.status_code}"
            raise exceptions.ApiException(err_msg)

        if len(r.json()) == 0:
            err_msg = f"customer not found for email='{email}'"
            raise exceptions.CustomerException(err_msg)

        data = r.json()[0]
        customer = cls(
            id=data["id"],
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
        )

        logger.debug("# assign customer address if it exists")
        try:
            customer.address = Address.from_customer_id(customer.id)
        except exceptions.AddressException:
            customer.address = None
        finally:
            return customer

    @classmethod
    def new_from_cli(cls, email, first_name, last_name):
        """Create customer instance using data supplied from CLI

        Args:
            email (str)         : new customer email
            first_name (str)    : new customer first name
            last_name (str)     : new customer last name

        Returns:
            Customer
        """

        # check if customer already exists
        logger.debug("# check if customer already exists")
        if Customer.email_exists(email=email):
            raise exceptions.CustomerException("email already in use")

        data = cls._http_create(email, first_name, last_name)

        return cls(
            id=data["id"],
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

    @classmethod
    def _http_create(cls, email, first_name, last_name):
        # TODO: all models will require http_create logic with slightly
        #  different endpoint and payload
        """Create new customer

        Args
            email (str)         : email
            first_name (str)    : first name
            last_name (str)     : last name
        """
        # make post request to api with new customer data
        logger.debug("# make post request to api with new customer data")
        payload = dict(email=email, first_name=first_name, last_name=last_name)
        r = requests_retry_session().post(cls.rest_endpoint, data=payload)
        return r.json()
