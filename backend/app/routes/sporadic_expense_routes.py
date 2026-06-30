from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user_model import User
from app.schemas.sporadic_expense_schema import SporadicExpenseCreate, SporadicExpenseRead
from app.services.auth_service import get_current_user
from app.services.sporadic_expense_service import (
    add_sporadic_expense,
    edit_sporadic_expense,
    list_sporadic_expenses,
    remove_sporadic_expense,
)

router = APIRouter(prefix="/sporadic-expenses", tags=["sporadic-expenses"])


@router.post("", response_model=SporadicExpenseRead, status_code=status.HTTP_201_CREATED)
def create_sporadic_expense_route(
    payload: SporadicExpenseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return add_sporadic_expense(
        db,
        user_id=current_user.id,
        description=payload.description,
        amount=payload.amount,
        currency=payload.currency,
        expense_date=payload.expense_date,
        category_id=payload.category_id,
    )


@router.get("", response_model=list[SporadicExpenseRead])
def get_sporadic_expenses(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return list_sporadic_expenses(db, current_user.id)


@router.put("/{expense_id}", response_model=SporadicExpenseRead)
def update_sporadic_expense_route(
    expense_id: int,
    payload: SporadicExpenseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return edit_sporadic_expense(
        db,
        user_id=current_user.id,
        expense_id=expense_id,
        description=payload.description,
        amount=payload.amount,
        currency=payload.currency,
        expense_date=payload.expense_date,
        category_id=payload.category_id,
    )


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sporadic_expense_route(
    expense_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    remove_sporadic_expense(db, current_user.id, expense_id)
