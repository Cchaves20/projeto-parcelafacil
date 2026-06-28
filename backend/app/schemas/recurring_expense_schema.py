from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.enums import Currency, Frequency


class RecurringExpensePeriodSchema(BaseModel):
    start_date: date
    end_date: date | None = None


class RecurringExpenseCreate(BaseModel):
    name: str
    amount: Decimal
    currency: Currency = Currency.BRL
    category_id: int | None = None
    frequency: Frequency = Frequency.MONTHLY
    billing_day: int | None = None
    weekdays: list[int] | None = None
    periods: list[RecurringExpensePeriodSchema]


class RecurringExpenseRead(BaseModel):
    id: int
    name: str
    amount: Decimal
    currency: Currency
    category_id: int | None
    frequency: Frequency
    billing_day: int | None
    weekdays: list[int] | None
    periods: list[RecurringExpensePeriodSchema]
    active: bool

    model_config = ConfigDict(from_attributes=True)
