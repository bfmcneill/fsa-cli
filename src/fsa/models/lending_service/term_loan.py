from fsa.models.account_type import AccountType
from fsa.models.customer.customer import Customer
from fsa.models.lending_service.lending_service import LendingService


class TermLoan(LendingService):
    """Term loan - credit service where upon creation the entire amount is dispursed (unlike a credit card where disbursements occure as customer requires"""

    account_type = AccountType.TERM_LOAN

    def __init__(
        self,
        id: int,
        account_type: AccountType,
        owner_id: int,
        rate: float,
        term: int,
        limit: float,
    ):
        super().__init__(
            id,
            account_type=account_type,
            customer_id=owner_id,
            rate=rate,
            limit=limit,
        )

        self.term = term
        self.disbursement(amount=self.limit, memo="loan funded")

    @classmethod
    def create(cls, email: str, rate: float, term: int, limit: float):
        """Create a new term loan

        Args
            email   : customer email
            rate    : interest rate
            term    : number of months
            limit   : approved loan amount

        Returns
            TermLoan
        """
        owner = Customer.from_api_using_email(email=email)

        data = cls._http_create(
            owner,
            cls.account_type,
            rate=rate,
            term=term,
            limt=limit,
        )

        return cls(
            data["id"],
            cls.account_type,
            owner.id,
            rate=rate,
            term=term,
            limit=limit,
        )
