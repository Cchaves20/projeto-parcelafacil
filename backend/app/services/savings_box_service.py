from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.enums import Currency
from app.models.savings_box_model import SavingsBox, SavingsTransaction
from app.repositories.savings_box_repository import (
    add_transaction,
    create_savings_box,
    delete_savings_box,
    delete_transaction,
    get_savings_box,
    get_transaction,
    list_savings_boxes_by_user,
)


def _compute_balance(box: SavingsBox) -> Decimal:
    return sum((t.amount for t in box.transactions), Decimal("0"))


def _attach_balance(box: SavingsBox) -> SavingsBox:
    box.balance = _compute_balance(box)
    return box


def add_savings_box(db: Session, user_id: int, name: str, currency: Currency, annual_rate: Decimal) -> SavingsBox:
    box = SavingsBox(user_id=user_id, name=name, currency=currency, annual_rate=annual_rate)
    box = create_savings_box(db, box)
    box.balance = Decimal("0")
    return box


def list_savings_boxes(db: Session, user_id: int) -> list[SavingsBox]:
    boxes = list_savings_boxes_by_user(db, user_id)
    return [_attach_balance(b) for b in boxes]


def edit_savings_box(db: Session, user_id: int, box_id: int, name: str, currency: Currency, annual_rate: Decimal) -> SavingsBox:
    box = get_savings_box(db, user_id, box_id)
    if not box:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Caixinha não encontrada")
    box.name = name
    box.currency = currency
    box.annual_rate = annual_rate
    db.commit()
    db.refresh(box)
    return _attach_balance(box)


def remove_savings_box(db: Session, user_id: int, box_id: int) -> None:
    box = get_savings_box(db, user_id, box_id)
    if not box:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Caixinha não encontrada")
    delete_savings_box(db, box)


def add_savings_transaction(db: Session, user_id: int, box_id: int, amount: Decimal, description: str | None) -> SavingsBox:
    box = get_savings_box(db, user_id, box_id)
    if not box:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Caixinha não encontrada")
    transaction = SavingsTransaction(box_id=box_id, amount=amount, description=description)
    add_transaction(db, transaction)
    db.refresh(box)
    return _attach_balance(box)


def remove_savings_transaction(db: Session, user_id: int, box_id: int, transaction_id: int) -> SavingsBox:
    box = get_savings_box(db, user_id, box_id)
    if not box:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Caixinha não encontrada")
    transaction = get_transaction(db, transaction_id, box_id)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transação não encontrada")
    delete_transaction(db, transaction)
    db.refresh(box)
    return _attach_balance(box)
