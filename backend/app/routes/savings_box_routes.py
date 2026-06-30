from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user_model import User
from app.schemas.savings_box_schema import (
    SavingsBoxCreate,
    SavingsBoxRead,
    SavingsBoxUpdate,
    SavingsTransactionCreate,
)
from app.services.auth_service import get_current_user
from app.services.savings_box_service import (
    add_savings_box,
    add_savings_transaction,
    edit_savings_box,
    list_savings_boxes,
    remove_savings_box,
    remove_savings_transaction,
)

router = APIRouter(prefix="/savings-boxes", tags=["savings-boxes"])


@router.post("", response_model=SavingsBoxRead, status_code=status.HTTP_201_CREATED)
def create_savings_box_route(
    payload: SavingsBoxCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return add_savings_box(db, current_user.id, payload.name, payload.currency, payload.annual_rate)


@router.get("", response_model=list[SavingsBoxRead])
def get_savings_boxes(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return list_savings_boxes(db, current_user.id)


@router.put("/{box_id}", response_model=SavingsBoxRead)
def update_savings_box_route(
    box_id: int,
    payload: SavingsBoxUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return edit_savings_box(db, current_user.id, box_id, payload.name, payload.currency, payload.annual_rate)


@router.delete("/{box_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_savings_box_route(
    box_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    remove_savings_box(db, current_user.id, box_id)


@router.post("/{box_id}/transactions", response_model=SavingsBoxRead)
def create_transaction_route(
    box_id: int,
    payload: SavingsTransactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return add_savings_transaction(db, current_user.id, box_id, payload.amount, payload.description)


@router.delete("/{box_id}/transactions/{transaction_id}", response_model=SavingsBoxRead)
def delete_transaction_route(
    box_id: int,
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return remove_savings_transaction(db, current_user.id, box_id, transaction_id)
