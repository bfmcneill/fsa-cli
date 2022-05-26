import requests
from loguru import logger
from fsa.models import account_type as account_type_enum
from fsa.models import customer
from fsa import exceptions, settings
from requests import exceptions as requests_exceptions


class Account:
    def __init__(
        self,
        account_id: int,
        account_type: account_type_enum.AccountType,
        owner: customer.Customer,
        **kwargs,
    ):
        self.id = account_id
        self.account_type = account_type
        self.owner = owner

    def serialize(self):
        """Serialize state"""
        return dict(
            id=self.id,
            account_type=self.account_type,
            owner_id=self.owner.customer_id,
        )

    def __repr__(self):
        return f"<Account id={self.id} account_type={self.account_type} owner_email={self.owner.email}>"

    @classmethod
    def from_id(cls, id):
        r = requests.get(f"{settings.BASE_URL}/account/{id}")
        data = r.json()
        return cls.__init__(**data)

    @classmethod
    def _http_create(self, **kwargs):
        """Create a new account

        Args
            account_type: AccountType
            owner: Customer

        Returns
            Account
        """
        owner = kwargs["owner"]
        account_type = kwargs["account_type"]
        payload = dict(account_type=account_type, owner_id=owner.customer_id)
        logger.debug(f"payload={payload}")

        try:
            r = requests.post(f"{settings.BASE_URL}/accounts", data=payload)
            if not r.ok():
                err_message = f"POST `/accounts` returned {r.status_code}"
                raise exceptions.ApiException(err_message)

        except requests_exceptions.ConnectionError:
            raise exceptions.ApiException(f"{settings.BASE_URL} is not responding")

        data = r.json()

        return Account(
            account_id=data["id"],
            account_type=account_type,
            owner=owner,
        )

    @classmethod
    def from_customer_email(cls, email, account_type: account_type_enum.AccountType):
        """Create an account linked to a specific customer

        Args:
            email (str)
            account_type (AccountType)

        Returns
            Customer
        """
        try:
            owner = customer.Customer.from_email(email=email)
            logger.debug(f"found customer: {owner}")
        except exceptions.DatabaseException as e:
            logger.warning("account creation failed")
            return None

        new_account = Account._http_create(account_type=account_type, owner=owner)
        logger.debug(f"created account: {new_account}")

    # def credit(self,record_date,amount,memo):
    #     ledger = ledger.Ledger(self.id)
    #     self.ledger.record(record_date,amount,memo)

    # def debit(self,record_date,amount,memo):
    #     self.ledger.record(record_date,amount,memo)

    # def history(self,after,before):
    #     self.ledger.search(after,before)
