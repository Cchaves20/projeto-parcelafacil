from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.enums import Currency
from app.schemas.installment_schema import InstallmentRead


class InstallmentPurchaseCreate(BaseModel):
    description: str
    total_amount: Decimal
    currency: Currency = Currency.BRL
    category_id: int | None = None
    installments_count: int
    first_due_date: date


class InstallmentPurchaseRead(BaseModel):
    id: int
    description: str
    total_amount: Decimal
    currency: Currency
    category_id: int | None
    installments_count: int
    first_due_date: date
    installments: list[InstallmentRead] = []

    model_config = ConfigDict(from_attributes=True)
