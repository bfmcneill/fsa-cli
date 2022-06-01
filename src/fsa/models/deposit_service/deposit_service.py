import logging
import pendulum
from fsa.exceptions import DepositServiceException
from fsa.models.account import Account
from fsa.models.account_type import AccountType

logger = logging.getLogger(__name__)


class DepositService(Account):
    """Depository services are used by customers to store their money"""

    def __init__(
        self,
        id: int,
        account_type: AccountType,
        customer_id: int,
    ):
        # TODO not sure if valid account typs is right design pattern, tried to set instance variable on super class but caused issues with unit testing deposit service and lending services
        super().__init__(
            id,
            account_type,
            customer_id,
            valid_account_types=[
                AccountType.CHECKING,
                AccountType.SAVINGS,
            ],
        )

    def deposit(self, amount: float, memo: str = "") -> dict:
        """Apply account deposit to ledger (credit)

        Args
            amount  : transaction amount
            memo    : transaction notes

        Returns
            json response as dict containing the ledger record data entered into system

        """
        self._validate_account_type_action("deposit")
        _amount = self.validate_money_amount(amount)

        # process deposit by appending a credit to ledger
        logger.debug("# process deposit by appending a credit to ledger")
        return self.ledger.append(
            self.id,
            pendulum.now(),
            credit=_amount,
            debit=0,
            memo=memo,
        )

    def withdraw(self, amount: float, memo: str = "") -> dict:
        """Apply account withdraw to ledger (debit)

        Args
            amount  : transaction amount
            memo    : transaction notes

        Returns
            json response as dict containing the ledger record data entered into system

        Raises
            DepositServiceException : raised to prevent negative balance
        """
        self._validate_account_type_action("withdraw")
        _amount = self.validate_money_amount(amount)
        _balance = self.ledger.balance

        if amount <= _balance:
            # process withdraw
            logger.debug("# process withdraw")
            return self.ledger.append(self.id, pendulum.now(), 0, amount, memo)

        raise DepositServiceException(f"reduce amount by {abs(_balance-amount)}")
