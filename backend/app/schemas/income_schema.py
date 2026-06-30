from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.enums import Currency


class IncomeCreate(BaseModel):
    description: str | None = None
    amount: Decimal
    currency: Currency = Currency.BRL
    payment_day: int | None = None
    start_date: date | None = None
    end_date: date | None = None


class IncomeRead(BaseModel):
    id: int
    description: str | None
    amount: Decimal
    currency: Currency
    payment_day: int | None
    start_date: date | None
    end_date: date | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
