from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user_model import User
from app.schemas.recurring_expense_schema import RecurringExpenseCreate, RecurringExpenseRead
from app.services.auth_service import get_current_user
from app.services.recurring_expense_service import (
    add_recurring_expense,
    list_recurring_expenses,
    remove_recurring_expense,
)

router = APIRouter(prefix="/recurring-expenses", tags=["recurring-expenses"])


@router.post("", response_model=RecurringExpenseRead, status_code=status.HTTP_201_CREATED)
def create_recurring_expense(
    payload: RecurringExpenseCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return add_recurring_expense(
        db,
        user_id=current_user.id,
        name=payload.name,
        amount=payload.amount,
        currency=payload.currency,
        billing_day=payload.billing_day,
        start_date=payload.start_date,
        end_date=payload.end_date,
        category_id=payload.category_id,
    )


@router.get("", response_model=list[RecurringExpenseRead])
def get_recurring_expenses(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return list_recurring_expenses(db, current_user.id)


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recurring_expense_route(
    expense_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    remove_recurring_expense(db, current_user.id, expense_id)
