from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.enums import Currency


class IncomeCreate(BaseModel):
    description: str | None = None
    amount: Decimal
    currency: Currency = Currency.BRL
    payment_day: int | None = None


class IncomeRead(BaseModel):
    id: int
    description: str | None
    amount: Decimal
    currency: Currency
    payment_day: int | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
