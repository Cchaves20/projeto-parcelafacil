from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.enums import Currency


class SavingsBoxCreate(BaseModel):
    name: str
    currency: Currency = Currency.BRL
    annual_rate: Decimal = Decimal("0")


class SavingsBoxUpdate(BaseModel):
    name: str
    currency: Currency
    annual_rate: Decimal


class SavingsTransactionCreate(BaseModel):
    amount: Decimal
    description: str | None = None


class SavingsTransactionRead(BaseModel):
    id: int
    amount: Decimal
    description: str | None
    transaction_date: datetime

    model_config = ConfigDict(from_attributes=True)


class SavingsBoxRead(BaseModel):
    id: int
    name: str
    currency: Currency
    annual_rate: Decimal
    balance: Decimal
    transactions: list[SavingsTransactionRead]

    model_config = ConfigDict(from_attributes=True)
