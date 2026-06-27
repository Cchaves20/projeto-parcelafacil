import enum


class Currency(str, enum.Enum):
    BRL = "BRL"
    USD = "USD"


class InstallmentStatus(str, enum.Enum):
    PENDING = "PENDING"
    PAID = "PAID"
