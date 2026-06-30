from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user_model import User
from app.schemas.income_schema import IncomeCreate, IncomeRead
from app.schemas.user_schema import UserRead
from app.services.auth_service import get_current_user
from app.services.income_service import add_income, edit_income, list_incomes, remove_income

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/me/incomes", response_model=IncomeRead, status_code=status.HTTP_201_CREATED)
def create_income(
    payload: IncomeCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return add_income(
        db,
        current_user.id,
        amount=payload.amount,
        currency=payload.currency,
        description=payload.description,
        payment_day=payload.payment_day,
        start_date=payload.start_date,
        end_date=payload.end_date,
    )


@router.get("/me/incomes", response_model=list[IncomeRead])
def get_incomes(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return list_incomes(db, current_user.id)


@router.put("/me/incomes/{income_id}", response_model=IncomeRead)
def update_income_route(
    income_id: int,
    payload: IncomeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return edit_income(
        db,
        current_user.id,
        income_id,
        amount=payload.amount,
        currency=payload.currency,
        description=payload.description,
        payment_day=payload.payment_day,
        start_date=payload.start_date,
        end_date=payload.end_date,
    )


@router.delete("/me/incomes/{income_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_income_route(
    income_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    remove_income(db, current_user.id, income_id)
