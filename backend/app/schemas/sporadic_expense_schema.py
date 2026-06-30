from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.enums import Currency


class SporadicExpenseCreate(BaseModel):
    description: str
    amount: Decimal
    currency: Currency = Currency.BRL
    expense_date: date
    category_id: int | None = None


class SporadicExpenseRead(BaseModel):
    id: int
    description: str
    amount: Decimal
    currency: Currency
    expense_date: date
    category_id: int | None
    category_name: str | None = None

    model_config = ConfigDict(from_attributes=True)
