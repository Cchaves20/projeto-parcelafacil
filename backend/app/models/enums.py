import enum


class Currency(str, enum.Enum):
    BRL = "BRL"
    USD = "USD"


class InstallmentStatus(str, enum.Enum):
    PENDING = "PENDING"
    PAID = "PAID"


class Frequency(str, enum.Enum):
    MONTHLY = "MONTHLY"
    WEEKLY = "WEEKLY"
