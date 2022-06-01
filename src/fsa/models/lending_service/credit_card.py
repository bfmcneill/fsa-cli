from fsa.models.account_type import AccountType
from fsa.models.customer.customer import Customer
from fsa.models.lending_service.lending_service import LendingService


class CreditCard(LendingService):
    """Credit card - credit service"""

    account_type = AccountType.CREDIT_CARD

    def __init__(
        self, id, account_type: AccountType, owner_id: int, rate: float, limit: float
    ):
        super().__init__(
            id,
            account_type=account_type,
            customer_id=owner_id,
            rate=rate,
            limit=limit,
        )

    @classmethod
    def create(cls, email: str, rate: float, limit: float):
        """Create a new credit card

        Args
            email   : customer email
            rate    : annual percentage rate
            limit   : approved credit limit

        Returns
            CreditCard
        """
        owner = Customer.from_api_using_email(email=email)
        data = cls._http_create(owner, AccountType.CREDIT_CARD, rate=rate, limit=limit)
        return cls(data["id"], cls.account_type, owner.id, rate=rate, limit=limit)
