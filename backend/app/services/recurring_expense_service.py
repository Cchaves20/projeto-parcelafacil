from datetime import date
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.enums import Currency
from app.models.recurring_expense_model import RecurringExpense
from app.repositories.recurring_expense_repository import (
    create_recurring_expense,
    delete_recurring_expense,
    get_recurring_expense,
    list_active_recurring_expenses_in_period,
    list_recurring_expenses_by_user,
)
from app.services.currency_service import to_brl
from app.utils.date_utils import next_billing_date


def add_recurring_expense(
    db: Session,
    user_id: int,
    name: str,
    amount: Decimal,
    currency: Currency,
    billing_day: int,
    start_date: date,
    end_date: date | None,
    category_id: int | None,
) -> RecurringExpense:
    if not 1 <= billing_day <= 31:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Dia de cobrança inválido")
    return create_recurring_expense(
        db,
        user_id=user_id,
        name=name,
        amount=amount,
        currency=currency,
        billing_day=billing_day,
        start_date=start_date,
        end_date=end_date,
        category_id=category_id,
    )


def list_recurring_expenses(db: Session, user_id: int) -> list[RecurringExpense]:
    return list_recurring_expenses_by_user(db, user_id)


def remove_recurring_expense(db: Session, user_id: int, expense_id: int) -> None:
    expense = get_recurring_expense(db, user_id, expense_id)
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gasto recorrente não encontrado")
    delete_recurring_expense(db, expense)


def total_recurring_expenses_brl_for_month(db: Session, user_id: int, year: int, month: int) -> Decimal:
    period_start = date(year, month, 1)
    period_end = date(year, month, 28)
    expenses = list_active_recurring_expenses_in_period(db, user_id, period_start, period_end)
    return sum((to_brl(expense.amount, expense.currency) for expense in expenses), Decimal("0"))


def expenses_due_in_period(db: Session, user_id: int, period_start: date, period_end: date) -> list[dict]:
    expenses = list_active_recurring_expenses_in_period(db, user_id, period_start, period_end)
    return [
        {"name": expense.name, "amount": expense.amount, "currency": expense.currency, "due_date": next_billing_date(period_start, expense.billing_day)}
        for expense in expenses
    ]
