from sqlalchemy.orm import Session, joinedload

from app.models.installment_purchase_model import InstallmentPurchase


def create_installment_purchase(db: Session, purchase: InstallmentPurchase) -> InstallmentPurchase:
    db.add(purchase)
    db.commit()
    db.refresh(purchase)
    return purchase


def list_installment_purchases_by_user(db: Session, user_id: int) -> list[InstallmentPurchase]:
    return (
        db.query(InstallmentPurchase)
        .options(joinedload(InstallmentPurchase.installments))
        .filter(InstallmentPurchase.user_id == user_id)
        .all()
    )


def get_installment_purchase(db: Session, user_id: int, purchase_id: int) -> InstallmentPurchase | None:
    return (
        db.query(InstallmentPurchase)
        .options(joinedload(InstallmentPurchase.installments))
        .filter(InstallmentPurchase.user_id == user_id, InstallmentPurchase.id == purchase_id)
        .first()
    )


def delete_installment_purchase(db: Session, purchase: InstallmentPurchase) -> None:
    db.delete(purchase)
    db.commit()
