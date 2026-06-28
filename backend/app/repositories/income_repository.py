from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.enums import Currency
from app.models.income_model import Income


def create_income(
    db: Session, user_id: int, amount: Decimal, currency: Currency, description: str | None, payment_day: int | None
) -> Income:
    income = Income(user_id=user_id, amount=amount, currency=currency, description=description, payment_day=payment_day)
    db.add(income)
    db.commit()
    db.refresh(income)
    return income


def list_incomes_by_user(db: Session, user_id: int) -> list[Income]:
    return db.query(Income).filter(Income.user_id == user_id).all()


def get_income(db: Session, user_id: int, income_id: int) -> Income | None:
    return db.query(Income).filter(Income.user_id == user_id, Income.id == income_id).first()


def update_income(
    db: Session, income: Income, amount: Decimal, currency: Currency, description: str | None, payment_day: int | None
) -> Income:
    income.amount = amount
    income.currency = currency
    income.description = description
    income.payment_day = payment_day
    db.commit()
    db.refresh(income)
    return income


def delete_income(db: Session, income: Income) -> None:
    db.delete(income)
    db.commit()
