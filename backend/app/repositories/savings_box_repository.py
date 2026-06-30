from sqlalchemy.orm import Session, joinedload

from app.models.savings_box_model import SavingsBox, SavingsTransaction


def create_savings_box(db: Session, box: SavingsBox) -> SavingsBox:
    db.add(box)
    db.commit()
    db.refresh(box)
    return box


def list_savings_boxes_by_user(db: Session, user_id: int) -> list[SavingsBox]:
    return (
        db.query(SavingsBox)
        .options(joinedload(SavingsBox.transactions))
        .filter(SavingsBox.user_id == user_id)
        .all()
    )


def get_savings_box(db: Session, user_id: int, box_id: int) -> SavingsBox | None:
    return (
        db.query(SavingsBox)
        .options(joinedload(SavingsBox.transactions))
        .filter(SavingsBox.user_id == user_id, SavingsBox.id == box_id)
        .first()
    )


def delete_savings_box(db: Session, box: SavingsBox) -> None:
    db.delete(box)
    db.commit()


def add_transaction(db: Session, transaction: SavingsTransaction) -> SavingsTransaction:
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


def get_transaction(db: Session, transaction_id: int, box_id: int) -> SavingsTransaction | None:
    return db.query(SavingsTransaction).filter(
        SavingsTransaction.id == transaction_id, SavingsTransaction.box_id == box_id
    ).first()


def delete_transaction(db: Session, transaction: SavingsTransaction) -> None:
    db.delete(transaction)
    db.commit()
