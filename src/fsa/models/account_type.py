from enum import Enum, unique


@unique
class AccountType(Enum):
    CHECKING = 1
    SAVINGS = 2
    CREDIT_CARD = 3
    TERM_LOAN = 4
