from fsa.settings import BASE_URL
from fsa import exceptions
import logging
from fsa.utils.request_utils import requests_retry_session

logger = logging.getLogger(__name__)


class Address:
    api_endpoint = f"{BASE_URL}/addresses"

    def __init__(self, id, customer_id, line1, line2, city, state_code, zip_code):
        self.id = id
        self.customer_id = customer_id
        self.line1 = line1
        self.line2 = line2
        self.city = city
        self.state_code = state_code
        self.zip_code = zip_code

    @classmethod
    def from_customer_id(cls, customer_id):
        """Create address instance built from API response filtered by customer id

        Args
            customer_id (int)   : customer id to look up in address collection

        Returns
            Address
        """
        params = dict(customer_id=customer_id)
        r = requests_retry_session().get(f"{cls.api_endpoint}", params=params)

        if not r.ok:
            err_msg = f"API request error: status_code=={r.status_code}"
            raise exceptions.ApiException(err_msg)

        if len(r.json()) == 0:
            logger.debug("customer address not found")
            raise exceptions.AddressException("customer address not found")

        data = r.json()[0]
        logger.debug("loading customer address from json response")
        return cls(
            data["id"],
            data["customer_id"],
            data["line1"],
            data.get("line2", None),
            data["city"],
            data["state_code"],
            data["zip_code"],
        )

    @classmethod
    def exists(cls, customer_id: int) -> tuple:
        """Determine if customer address exists

        Args
            customer_id: the customer id to update

        Returns:
            tuple(exists:bool,address:Address)

        """
        exists = True
        address = None
        try:
            address = cls.from_customer_id(customer_id)
        except exceptions.AddressException:
            exists = False
        return exists, address

    @staticmethod
    def _http_post(url, data):
        logger.debug("create address record")
        return requests_retry_session().post(url, data=data)

    @staticmethod
    def _http_patch(url, data):
        logger.debug("update address record")
        return requests_retry_session().patch(url, data=data)

    @staticmethod
    def _dispatch_http(url, method, payload):
        req = {
            "POST": Address._http_post,
            "PATCH": Address._http_patch,
        }
        logger.debug(f"dispatching http request: {method}")
        res = req[method](url, data=payload)

        if not res.ok:
            raise exceptions.ApiException(f"{method} {url}: {res.status_code}")

        return res.json()

    @classmethod
    def upsert(cls, customer_id, data):

        exists, address = cls.exists(customer_id)
        payload = dict(**data)

        method = "PATCH" if exists else "POST"
        url = f"{cls.api_endpoint}/{address.id}" if exists else cls.api_endpoint

        if not exists:
            payload["customer_id"] = customer_id

        Address._dispatch_http(url, method, payload)

    @classmethod
    def from_cli(cls, customer_id, line1, line2, city, state_code, zip_code):
        payload = dict(
            line1=line1,
            line2=line2,
            city=city,
            state_code=state_code,
            zip_code=zip_code,
        )

        exists, address_id = address_id = cls.exists(customer_id)

        if exists:
            logger.debug("# update customer address")
            url = f"{cls.api_endpoint}/{address_id}"
            method = "PATCH"
        else:
            logger.debug("# create customer address")
            url = cls.api_endpoint
            method = "POST"
            payload["customer_id"] = customer_id

        data = cls.dispatch_http(url, method, payload)

        return cls(
            id=data["id"],
            customer_id=data["customer_id"],
            line1=data["line1"],
            line2=data["line2"],
            city=data["city"],
            state_code=data["state_code"],
            zip_code=data["zip_code"],
        )
