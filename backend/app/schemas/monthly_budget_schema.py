from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class MonthlyBudgetCreate(BaseModel):
    year: int
    month: int
    limit_amount: Decimal


class MonthlyBudgetRead(BaseModel):
    id: int
    year: int
    month: int
    limit_amount: Decimal

    model_config = ConfigDict(from_attributes=True)
