from sqlalchemy.orm import Session

from app.models.sporadic_expense_model import SporadicExpense


def create_sporadic_expense(db: Session, expense: SporadicExpense) -> SporadicExpense:
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


def list_sporadic_expenses_by_user(db: Session, user_id: int) -> list[SporadicExpense]:
    return db.query(SporadicExpense).filter(SporadicExpense.user_id == user_id).order_by(SporadicExpense.expense_date.desc()).all()


def get_sporadic_expense(db: Session, user_id: int, expense_id: int) -> SporadicExpense | None:
    return db.query(SporadicExpense).filter(SporadicExpense.user_id == user_id, SporadicExpense.id == expense_id).first()


def delete_sporadic_expense(db: Session, expense: SporadicExpense) -> None:
    db.delete(expense)
    db.commit()
