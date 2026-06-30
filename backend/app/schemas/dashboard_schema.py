from decimal import Decimal

from pydantic import BaseModel


class MonthlySummary(BaseModel):
    year: int
    month: int
    monthly_income_brl: Decimal
    recurring_expenses_brl: Decimal
    installments_brl: Decimal
    sporadic_expenses_brl: Decimal
    total_committed_brl: Decimal
    committed_percentage: Decimal
    exchange_rate_usd_brl: Decimal
