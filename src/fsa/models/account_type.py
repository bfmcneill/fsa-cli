import enum


@enum.unique
class AccountType(enum.Enum):
    CHECKING = 1
    SAVINGS = 2
    CREDIT_CARD = 3
    TERM_LOAN = 4
