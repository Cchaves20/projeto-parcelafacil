from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user_model import User
from app.schemas.installment_purchase_schema import InstallmentPurchaseCreate, InstallmentPurchaseRead
from app.services.auth_service import get_current_user
from app.services.installment_purchase_service import (
    add_installment_purchase,
    list_installment_purchases,
    remove_installment_purchase,
)

router = APIRouter(prefix="/installment-purchases", tags=["installment-purchases"])


@router.post("", response_model=InstallmentPurchaseRead, status_code=status.HTTP_201_CREATED)
def create_installment_purchase(
    payload: InstallmentPurchaseCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return add_installment_purchase(
        db,
        user_id=current_user.id,
        description=payload.description,
        total_amount=payload.total_amount,
        currency=payload.currency,
        installments_count=payload.installments_count,
        first_due_date=payload.first_due_date,
        category_id=payload.category_id,
    )


@router.get("", response_model=list[InstallmentPurchaseRead])
def get_installment_purchases(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return list_installment_purchases(db, current_user.id)


@router.delete("/{purchase_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_installment_purchase_route(
    purchase_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    remove_installment_purchase(db, current_user.id, purchase_id)
