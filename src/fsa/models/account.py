from __future__ import annotations
from typing import Union, List
import logging

from requests import exceptions as requests_exceptions
from fsa.utils import request_utils as http
from fsa.models.account_type import AccountType
from fsa.models.customer.customer import Customer
from fsa.models.ledger import Ledger
from fsa import exceptions, settings

logger = logging.getLogger(__name__)


class Account:

    api_endpoint = f"{settings.BASE_URL}/accounts"

    def __init__(
        self,
        id: int,
        account_type: AccountType,
        customer_id: int,
        valid_account_types: List[AccountType] = None,
    ):
        """Account initializer

        Args:
            id              : unique account id
            account_type    : standard account options stored in enum
            customer_id     : customer id who owns the account

        """
        self.id = id
        self.account_type = account_type
        self._customer_id = customer_id
        self._valid_account_types = valid_account_types

    @property
    def owner(self) -> Customer:
        """owner property is the customer id reference for the account

        Returns:
            Customer object instance
        """
        return Customer.from_id(self._customer_id)

    @property
    def ledger(self) -> Ledger:
        """Property associates an account instance with ledger instance

        Returns:
            Ledger which gives Account ability to transact, check balance, generate activity report, etc
        """
        return Ledger(self)

    def __repr__(self):
        return f"{__class__.__name__}(id={self.id}, account_type={self.account_type}, _customer_id={self._customer_id})"

    @classmethod
    def from_account_id(cls, account_id: Union[str, int]) -> Account:
        """Create account instance from account id

        Args
            account_id  : The account id

        Returns
            Account

        Raises
            DepositoryServiceException: error when no account is found
        """
        url = f"{cls.api_endpoint}/{account_id}"
        res = http.requests_retry_session().get(url)
        data = res.json()
        if not bool(data):
            raise exceptions.DepositServiceException("Account not found")
        return cls(
            id=data["id"],
            account_type=AccountType[data["account_type"]],
            customer_id=data["owner_id"],
        )

    @staticmethod
    def validate_money_amount(amount: Union[int, float]) -> float:
        """Amount must be numeric, non-zero, and positive

        Args:
            amount  : the amount to validate

        Returns:
            the validated amount as float

        Raises:
            AccountException: raised if amount is not numeric, non-zero or negative
        """
        try:
            _amount = float(amount)
            if _amount > 0:
                return _amount
            raise exceptions.AccountException("positive amount required")
        except ValueError:
            raise exceptions.AccountException("amount must be numeric")

    @classmethod
    def _http_create(
        cls,
        customer: Customer,
        account_type: AccountType,
        **kwargs,
    ) -> dict:
        """API POST request that creates a new account

        Args
            customer        : customer the account belongs to
            account_type    : type of account being created (checking, savings, loan, credit card)
            **kwargs        : account specific attributes - interest rate,term, loan amount, etc.

        Returns
            data contained within http post response

        Raises
            CustomerException: raised if customer does not have address established
            ApiException:
                1) raised if server can't be reached
                2) raised if POST request is not successful
        """
        # validate customer address
        logger.debug("# validate customer address")
        if not customer.address:
            err_msg = "customer requires address before creating accounts"
            raise exceptions.CustomerException(err_msg)

        payload = dict(
            account_type=account_type.name,
            owner_id=customer.id,
            **kwargs,
        )

        try:
            r = http.requests_retry_session().post(cls.api_endpoint, data=payload)
            logger.debug(f"POST {cls.api_endpoint} (status_code: {r.status_code})")
            if not r.ok:
                err_message = "error creating account"
                raise exceptions.ApiException(err_message)

        except requests_exceptions.ConnectionError:
            # POST request error
            err_msg = f"{settings.BASE_URL} is not responding"
            logger.debug(err_msg)
            raise exceptions.ApiException(err_msg)

        return r.json()

    def create(self) -> Account:
        """stub for creating an account"""
        pass

    def _validate_account_type_action(self, action: str) -> bool:
        """Verifies the action is permitted.

        Arg:
            TODO: calling instance type could help eliminate need to provide arg
            action  : a short description of the action which helps the error message be clear

        Returns
            true if no exception is raised

        Raises
            LedgerException:
                raised when ledger operation is being applied to the wrong account type.
                i.e. savings accounts can't be the target of a loan payment

        """
        if not self._valid_account_types:
            # this error should never be triggered, Account must be subclassed
            raise exceptions.AccountException("Account must be subclassed")

        if self.account_type not in self._valid_account_types:
            logger.debug(f"{self.account_type} can not take {action}")
            err_msg = f"{self.account_type.name} can not take action={action}"
            raise exceptions.LedgerExecption(err_msg)
        return True
