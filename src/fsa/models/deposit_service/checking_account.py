from __future__ import annotations  # required to type @classmethod
import logging
from fsa.models.account_type import AccountType
from fsa.models.customer.customer import Customer
from fsa.models.deposit_service.deposit_service import DepositService

logger = logging.getLogger(__name__)


class CheckingAccount(DepositService):
    """Deposit service - Checking Account"""

    account_type = AccountType.CHECKING

    @classmethod
    def create(cls, email: str) -> CheckingAccount:
        """Create a new checking account for a specific customer

        Args
            email   : customer email the account will be linked to

        Returns
            CheckingAccount
        """

        # look up customer by email
        logger.debug("# look up customer by email")
        customer = Customer.from_api_using_email(email=email)

        # create customer account
        logger.debug("# create customer account")
        data = cls._http_create(customer, cls.account_type)

        return cls(data["id"], cls.account_type, customer.id)
