from datetime import date
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.enums import Currency
from app.models.installment_model import Installment
from app.models.installment_purchase_model import InstallmentPurchase
from app.repositories.installment_purchase_repository import (
    create_installment_purchase,
    delete_installment_purchase,
    get_installment_purchase,
    list_installment_purchases_by_user,
)
from app.utils.date_utils import add_months
from app.utils.money_utils import split_into_installments


def add_installment_purchase(
    db: Session,
    user_id: int,
    description: str,
    total_amount: Decimal,
    currency: Currency,
    installments_count: int,
    first_due_date: date,
    category_id: int | None,
) -> InstallmentPurchase:
    if installments_count < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Número de parcelas inválido")

    purchase = InstallmentPurchase(
        user_id=user_id,
        description=description,
        total_amount=total_amount,
        currency=currency,
        installments_count=installments_count,
        first_due_date=first_due_date,
        category_id=category_id,
    )

    installment_amounts = split_into_installments(total_amount, installments_count)
    purchase.installments = [
        Installment(number=index + 1, amount=amount, due_date=add_months(first_due_date, index))
        for index, amount in enumerate(installment_amounts)
    ]

    return create_installment_purchase(db, purchase)


def list_installment_purchases(db: Session, user_id: int) -> list[InstallmentPurchase]:
    return list_installment_purchases_by_user(db, user_id)


def remove_installment_purchase(db: Session, user_id: int, purchase_id: int) -> None:
    purchase = get_installment_purchase(db, user_id, purchase_id)
    if not purchase:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Compra parcelada não encontrada")
    delete_installment_purchase(db, purchase)


def toggle_installment_status(db: Session, user_id: int, purchase_id: int, installment_id: int) -> Installment:
    from app.models.enums import InstallmentStatus
    purchase = get_installment_purchase(db, user_id, purchase_id)
    if not purchase:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Compra parcelada não encontrada")
    installment = next((i for i in purchase.installments if i.id == installment_id), None)
    if not installment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parcela não encontrada")
    installment.status = InstallmentStatus.PAID if installment.status == InstallmentStatus.PENDING else InstallmentStatus.PENDING
    db.commit()
    db.refresh(installment)
    return installment
