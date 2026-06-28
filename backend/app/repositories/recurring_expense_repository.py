from datetime import date

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.recurring_expense_model import RecurringExpense
from app.models.recurring_expense_period_model import RecurringExpensePeriod


def create_recurring_expense(db: Session, user_id: int, periods: list[dict], **fields) -> RecurringExpense:
    expense = RecurringExpense(user_id=user_id, **fields)
    expense.periods = [RecurringExpensePeriod(**period) for period in periods]
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


def list_recurring_expenses_by_user(db: Session, user_id: int) -> list[RecurringExpense]:
    return db.query(RecurringExpense).filter(RecurringExpense.user_id == user_id).all()


def list_active_recurring_expenses_in_period(
    db: Session, user_id: int, period_start: date, period_end: date
) -> list[RecurringExpense]:
    return (
        db.query(RecurringExpense)
        .join(RecurringExpensePeriod)
        .filter(
            RecurringExpense.user_id == user_id,
            RecurringExpense.active.is_(True),
            RecurringExpensePeriod.start_date <= period_end,
            or_(RecurringExpensePeriod.end_date.is_(None), RecurringExpensePeriod.end_date >= period_start),
        )
        .distinct()
        .all()
    )


def get_recurring_expense(db: Session, user_id: int, expense_id: int) -> RecurringExpense | None:
    return (
        db.query(RecurringExpense)
        .filter(RecurringExpense.user_id == user_id, RecurringExpense.id == expense_id)
        .first()
    )


def update_recurring_expense(
    db: Session, expense: RecurringExpense, periods: list[dict], **fields
) -> RecurringExpense:
    for key, value in fields.items():
        setattr(expense, key, value)
    expense.periods = [RecurringExpensePeriod(**period) for period in periods]
    db.commit()
    db.refresh(expense)
    return expense


def delete_recurring_expense(db: Session, expense: RecurringExpense) -> None:
    db.delete(expense)
    db.commit()
