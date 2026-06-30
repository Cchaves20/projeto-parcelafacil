from decimal import Decimal

from sqlalchemy.orm import Session

from app.repositories.installment_repository import list_installments_in_period
from app.repositories.sporadic_expense_repository import list_sporadic_expenses_in_period
from app.schemas.dashboard_schema import MonthlySummary
from app.services.currency_service import get_usd_to_brl_rate, to_brl
from app.services.income_service import total_monthly_income_brl
from app.services.recurring_expense_service import total_recurring_expenses_brl_for_month
from app.utils.date_utils import month_range
from app.utils.money_utils import round_money


def total_installments_brl_for_month(db: Session, user_id: int, year: int, month: int) -> Decimal:
    period_start, period_end = month_range(year, month)
    installments = list_installments_in_period(db, user_id, period_start, period_end)
    return sum((to_brl(installment.amount, installment.purchase.currency) for installment in installments), Decimal("0"))


def total_sporadic_expenses_brl_for_month(db: Session, user_id: int, year: int, month: int) -> Decimal:
    period_start, period_end = month_range(year, month)
    expenses = list_sporadic_expenses_in_period(db, user_id, period_start, period_end)
    return sum((to_brl(e.amount, e.currency) for e in expenses), Decimal("0"))


def get_monthly_summary(db: Session, user_id: int, year: int, month: int) -> MonthlySummary:
    income_brl = total_monthly_income_brl(db, user_id, year, month)
    recurring_brl = total_recurring_expenses_brl_for_month(db, user_id, year, month)
    installments_brl = total_installments_brl_for_month(db, user_id, year, month)
    sporadic_brl = total_sporadic_expenses_brl_for_month(db, user_id, year, month)
    total_committed = recurring_brl + installments_brl + sporadic_brl

    committed_percentage = round_money((total_committed / income_brl) * 100) if income_brl > 0 else Decimal("0")

    return MonthlySummary(
        year=year,
        month=month,
        monthly_income_brl=round_money(income_brl),
        recurring_expenses_brl=round_money(recurring_brl),
        installments_brl=round_money(installments_brl),
        sporadic_expenses_brl=round_money(sporadic_brl),
        total_committed_brl=round_money(total_committed),
        committed_percentage=committed_percentage,
        exchange_rate_usd_brl=get_usd_to_brl_rate(),
    )
