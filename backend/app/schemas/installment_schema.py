from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.enums import InstallmentStatus


class InstallmentRead(BaseModel):
    id: int
    number: int
    amount: Decimal
    due_date: date
    status: InstallmentStatus

    model_config = ConfigDict(from_attributes=True)
