from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.enums import Currency
from app.models.income_model import Income
from app.repositories.income_repository import (
    create_income,
    delete_income,
    get_income,
    list_incomes_by_user,
    update_income,
)
from app.services.currency_service import to_brl


def add_income(
    db: Session,
    user_id: int,
    amount: Decimal,
    currency: Currency,
    description: str | None,
    payment_day: int | None = None,
) -> Income:
    if payment_day is not None and not 1 <= payment_day <= 31:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Dia de recebimento inválido")
    return create_income(
        db, user_id=user_id, amount=amount, currency=currency, description=description, payment_day=payment_day
    )


def list_incomes(db: Session, user_id: int) -> list[Income]:
    return list_incomes_by_user(db, user_id)


def edit_income(
    db: Session,
    user_id: int,
    income_id: int,
    amount: Decimal,
    currency: Currency,
    description: str | None,
    payment_day: int | None = None,
) -> Income:
    income = get_income(db, user_id, income_id)
    if not income:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Renda não encontrada")
    if payment_day is not None and not 1 <= payment_day <= 31:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Dia de recebimento inválido")
    return update_income(db, income, amount=amount, currency=currency, description=description, payment_day=payment_day)


def remove_income(db: Session, user_id: int, income_id: int) -> None:
    income = get_income(db, user_id, income_id)
    if not income:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Renda não encontrada")
    delete_income(db, income)


def total_monthly_income_brl(db: Session, user_id: int) -> Decimal:
    incomes = list_incomes_by_user(db, user_id)
    return sum((to_brl(income.amount, income.currency) for income in incomes), Decimal("0"))
