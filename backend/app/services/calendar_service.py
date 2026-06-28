from datetime import date

from sqlalchemy.orm import Session

from app.repositories.installment_repository import list_installments_in_period
from app.services.recurring_expense_service import expenses_due_in_period


def get_due_items(db: Session, user_id: int, period_start: date, period_end: date) -> list[dict]:
    items = []

    for expense in expenses_due_in_period(db, user_id, period_start, period_end):
        items.append({"type": "recurring_expense", **expense})

    for installment in list_installments_in_period(db, user_id, period_start, period_end):
        items.append(
            {
                "type": "installment",
                "name": f"{installment.purchase.description} ({installment.number}/{installment.purchase.installments_count})",
                "amount": installment.amount,
                "currency": installment.purchase.currency,
                "due_date": installment.due_date,
            }
        )

    return sorted(items, key=lambda item: item["due_date"])
