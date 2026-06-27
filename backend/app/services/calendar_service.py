from datetime import date

from sqlalchemy.orm import Session

from app.repositories.installment_repository import list_installments_in_period
from app.repositories.recurring_expense_repository import list_active_recurring_expenses_in_period
from app.utils.date_utils import next_billing_date


def get_due_items(db: Session, user_id: int, period_start: date, period_end: date) -> list[dict]:
    items = []

    for expense in list_active_recurring_expenses_in_period(db, user_id, period_start, period_end):
        items.append(
            {
                "type": "recurring_expense",
                "name": expense.name,
                "amount": expense.amount,
                "currency": expense.currency,
                "due_date": next_billing_date(period_start, expense.billing_day),
            }
        )

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
