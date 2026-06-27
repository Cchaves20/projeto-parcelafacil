from datetime import date

from sqlalchemy.orm import Session

from app.models.recurring_expense_model import RecurringExpense


def create_recurring_expense(db: Session, user_id: int, **fields) -> RecurringExpense:
    expense = RecurringExpense(user_id=user_id, **fields)
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
        .filter(
            RecurringExpense.user_id == user_id,
            RecurringExpense.active.is_(True),
            RecurringExpense.start_date <= period_end,
            (RecurringExpense.end_date.is_(None)) | (RecurringExpense.end_date >= period_start),
        )
        .all()
    )


def get_recurring_expense(db: Session, user_id: int, expense_id: int) -> RecurringExpense | None:
    return (
        db.query(RecurringExpense)
        .filter(RecurringExpense.user_id == user_id, RecurringExpense.id == expense_id)
        .first()
    )


def delete_recurring_expense(db: Session, expense: RecurringExpense) -> None:
    db.delete(expense)
    db.commit()
