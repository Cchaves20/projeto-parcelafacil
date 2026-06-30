from datetime import date
import calendar

from sqlalchemy.orm import Session

from app.repositories.installment_repository import list_installments_in_period
from app.repositories.savings_box_repository import list_savings_boxes_by_user
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

    for box in list_savings_boxes_by_user(db, user_id):
        if box.monthly_deposit_amount and box.monthly_deposit_day:
            current = date(period_start.year, period_start.month, 1)
            while current <= period_end:
                last_day = calendar.monthrange(current.year, current.month)[1]
                deposit_day = min(box.monthly_deposit_day, last_day)
                deposit_date = date(current.year, current.month, deposit_day)
                if period_start <= deposit_date <= period_end:
                    items.append(
                        {
                            "type": "savings_deposit",
                            "name": f"Aporte — {box.name}",
                            "amount": box.monthly_deposit_amount,
                            "currency": box.currency,
                            "due_date": deposit_date,
                        }
                    )
                if current.month == 12:
                    current = date(current.year + 1, 1, 1)
                else:
                    current = date(current.year, current.month + 1, 1)

    return sorted(items, key=lambda item: item["due_date"])
