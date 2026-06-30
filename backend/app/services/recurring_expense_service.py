from datetime import date
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.enums import Currency, Frequency
from app.models.recurring_expense_model import RecurringExpense
from app.repositories.recurring_expense_repository import (
    create_recurring_expense,
    delete_recurring_expense,
    get_recurring_expense,
    list_active_recurring_expenses_in_period,
    list_recurring_expenses_by_user,
    update_recurring_expense,
)
from app.services.currency_service import to_brl
from app.utils.date_utils import month_range, monthly_occurrences, weekday_occurrences


def _validate_recurring_expense(
    frequency: Frequency, billing_day: int | None, weekdays: list[int] | None, periods: list[dict]
) -> tuple[int | None, list[int] | None]:
    if not periods:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Informe ao menos um período ativo")
    for period in periods:
        if period["end_date"] and period["end_date"] < period["start_date"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Período inválido")

    if frequency == Frequency.MONTHLY:
        if billing_day is None or not 1 <= billing_day <= 31:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Dia de cobrança inválido")
        weekdays = None
    else:
        if not weekdays or any(not 0 <= day <= 6 for day in weekdays):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Dias da semana inválidos")
        billing_day = None

    return billing_day, weekdays


def add_recurring_expense(
    db: Session,
    user_id: int,
    name: str,
    amount: Decimal,
    currency: Currency,
    frequency: Frequency,
    billing_day: int | None,
    weekdays: list[int] | None,
    periods: list[dict],
    category_id: int | None,
) -> RecurringExpense:
    billing_day, weekdays = _validate_recurring_expense(frequency, billing_day, weekdays, periods)

    return create_recurring_expense(
        db,
        user_id=user_id,
        name=name,
        amount=amount,
        currency=currency,
        frequency=frequency,
        billing_day=billing_day,
        weekdays=weekdays,
        periods=periods,
        category_id=category_id,
    )


def list_recurring_expenses(db: Session, user_id: int) -> list[RecurringExpense]:
    return list_recurring_expenses_by_user(db, user_id)


def edit_recurring_expense(
    db: Session,
    user_id: int,
    expense_id: int,
    name: str,
    amount: Decimal,
    currency: Currency,
    frequency: Frequency,
    billing_day: int | None,
    weekdays: list[int] | None,
    periods: list[dict],
    category_id: int | None,
) -> RecurringExpense:
    expense = get_recurring_expense(db, user_id, expense_id)
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gasto recorrente não encontrado")

    billing_day, weekdays = _validate_recurring_expense(frequency, billing_day, weekdays, periods)

    return update_recurring_expense(
        db,
        expense,
        periods=periods,
        name=name,
        amount=amount,
        currency=currency,
        frequency=frequency,
        billing_day=billing_day,
        weekdays=weekdays,
        category_id=category_id,
    )


def remove_recurring_expense(db: Session, user_id: int, expense_id: int) -> None:
    expense = get_recurring_expense(db, user_id, expense_id)
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gasto recorrente não encontrado")
    delete_recurring_expense(db, expense)


def expense_occurrences_in_range(expense: RecurringExpense, range_start: date, range_end: date) -> list[date]:
    occurrences: set[date] = set()
    for period in expense.periods:
        effective_start = max(period.start_date, range_start)
        effective_end = min(period.end_date, range_end) if period.end_date else range_end
        if effective_start > effective_end:
            continue
        if expense.frequency == Frequency.WEEKLY:
            for weekday in expense.weekdays or []:
                occurrences.update(weekday_occurrences(effective_start, effective_end, weekday))
        else:
            occurrences.update(monthly_occurrences(effective_start, effective_end, expense.billing_day))
    return sorted(occurrences)


def effective_amount_per_occurrence(expense: RecurringExpense) -> Decimal:
    """For weekly expenses the stored amount is the total weekly budget;
    divide by number of selected weekdays to get the per-occurrence cost."""
    if expense.frequency == Frequency.WEEKLY and expense.weekdays:
        return expense.amount / Decimal(len(expense.weekdays))
    return expense.amount


def total_recurring_expenses_brl_for_month(db: Session, user_id: int, year: int, month: int) -> Decimal:
    period_start, period_end = month_range(year, month)
    expenses = list_active_recurring_expenses_in_period(db, user_id, period_start, period_end)
    total = Decimal("0")
    for expense in expenses:
        occurrences = expense_occurrences_in_range(expense, period_start, period_end)
        total += to_brl(effective_amount_per_occurrence(expense), expense.currency) * len(occurrences)
    return total


def expenses_due_in_period(db: Session, user_id: int, period_start: date, period_end: date) -> list[dict]:
    expenses = list_active_recurring_expenses_in_period(db, user_id, period_start, period_end)
    items = []
    for expense in expenses:
        amount_per_occurrence = effective_amount_per_occurrence(expense)
        for due_date in expense_occurrences_in_range(expense, period_start, period_end):
            items.append({"name": expense.name, "amount": amount_per_occurrence, "currency": expense.currency, "due_date": due_date})
    return items
