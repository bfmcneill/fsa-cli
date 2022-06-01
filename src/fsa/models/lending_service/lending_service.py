import logging
import pendulum
from fsa import exceptions
from fsa.models.account import Account
from fsa.models.account_type import AccountType

logger = logging.getLogger(__name__)


class LendingService(Account):
    """Lending services are used by customers to leverage bank money"""

    def __init__(
        self,
        id: int,
        account_type: AccountType,
        customer_id: int,
        rate: float,
        limit: float,
    ):
        # TODO not sure if storing valid account type for each instance in the super class is right design pattern,
        #  tried to set instance variable on super class to None then override it in the subclass but
        #  ran into issues with unit testing deposit service and lending services assertions
        #  on valid account type actions unless the current design pattern was used.
        super().__init__(
            id,
            account_type,
            customer_id,
            valid_account_types=[
                AccountType.CREDIT_CARD,
                AccountType.TERM_LOAN,
            ],
        )
        self.rate = rate
        self.limit = limit

    def payment(self, amount: float, memo: str = ""):
        """Apply a lending service payment to a ledger (debit)

        Args
            amount  : transaction amount
            memo    : transaction notes

        Returns
            json response as dict containing the ledger record data entered into system

        Raises
            LendingServiceException : raised to prevent overpayment
        """
        self._validate_account_type_action("payment")
        _amount = self.validate_money_amount(amount)
        _balance = self.ledger.balance

        # prevent overpayment
        if _amount > self.ledger.balance:
            err_msg = (
                f"overpayment not allowed, reduce amount by {abs(_balance-amount)}"
            )
            raise exceptions.LedgerExecption(err_msg)

        # process payment by appending a credit to ledger
        logger.debug("# process payment by appending a credit to ledger")
        return self.ledger.append(
            self.id,
            pendulum.now(),
            credit=0,
            debit=_amount,
            memo=memo,
        )

    def disbursement(self, amount: float, memo: str = ""):
        """Apply lending service disbursement to ledger (credit)
        Disbursement is the action a customer takes to `use` credit issued by bank,

        Args
            amount  : transaction amount
            memo    : transaction notes

        Returns
            json response as dict containing the ledger record data entered into system

        Raises
            LendingServiceException : raised to prevent using more credit than what customer was approved for


        """
        self._validate_account_type_action("disbursement")
        _amount = self.validate_money_amount(amount)
        _balance_after_disbursement = _amount + self.ledger.balance

        if (self.account_type == AccountType.TERM_LOAN) and self.ledger.balance > 0:
            # TODO: not sure this is a good design pattern for disabling a disbursement action after funding loan?
            #  It seems odd that the super class would handle a subclass scenario but it also seems odd that method
            #  would be overridden in subclass with nearly the same code but slightly different implementation
            # once loan is funded disbursement action is no longer permitted
            err_msg = "Loan has been funded already, disbursement action not permitted"
            raise exceptions.LendingServiceException(err_msg)

        if _balance_after_disbursement > self.limit:
            err_msg = f"balance can not exceed approved limit, "
            err_msg += f"reduce amount by {abs(_balance_after_disbursement-self.limit)}"
            raise exceptions.LendingServiceException(err_msg)

        # process disbursement
        logger.debug("# process disbursement by appending a debit to ledger")
        return self.ledger.append(
            self.id,
            pendulum.now(),
            credit=_amount,
            debit=0,
            memo=memo,
        )
