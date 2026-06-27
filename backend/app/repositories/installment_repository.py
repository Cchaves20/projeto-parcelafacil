from datetime import date

from sqlalchemy.orm import Session, joinedload

from app.models.installment_model import Installment
from app.models.installment_purchase_model import InstallmentPurchase


def list_installments_in_period(db: Session, user_id: int, period_start: date, period_end: date) -> list[Installment]:
    return (
        db.query(Installment)
        .join(InstallmentPurchase)
        .options(joinedload(Installment.purchase))
        .filter(
            InstallmentPurchase.user_id == user_id,
            Installment.due_date >= period_start,
            Installment.due_date <= period_end,
        )
        .all()
    )
