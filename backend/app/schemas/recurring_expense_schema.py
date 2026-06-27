from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.enums import Currency


class RecurringExpenseCreate(BaseModel):
    name: str
    amount: Decimal
    currency: Currency = Currency.BRL
    category_id: int | None = None
    billing_day: int
    start_date: date
    end_date: date | None = None


class RecurringExpenseRead(BaseModel):
    id: int
    name: str
    amount: Decimal
    currency: Currency
    category_id: int | None
    billing_day: int
    start_date: date
    end_date: date | None
    active: bool

    model_config = ConfigDict(from_attributes=True)
