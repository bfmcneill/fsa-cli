from fsa.models.account_type import AccountType
from fsa.models.customer.customer import Customer
from fsa.models.deposit_service.deposit_service import DepositService


class SavingsAccount(DepositService):
    """Deposit service - savings account"""

    account_type = AccountType.SAVINGS

    def __init__(self, id, account_type: AccountType, owner_id: int, rate: float):
        super().__init__(id, account_type=account_type, customer_id=owner_id)
        self.rate = rate

    @classmethod
    def create(cls, email: str, rate: float):
        """Create a new savings account for a specific customer

        Args
            email   : email address
            rate    : interest rate between 0 and 1
        """
        owner = Customer.from_api_using_email(email=email)

        data = cls._http_create(owner, cls.account_type, rate=rate)
        return cls(data["id"], cls.account_type, owner.id, rate)
