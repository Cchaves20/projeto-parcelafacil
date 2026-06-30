from datetime import date
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
from app.utils.date_utils import month_range


def _validate(payment_day: int | None, start_date: date | None, end_date: date | None) -> None:
    if payment_day is not None and not 1 <= payment_day <= 31:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Dia de recebimento inválido")
    if start_date and end_date and end_date < start_date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Data de início deve ser anterior à data de fim")


def add_income(
    db: Session,
    user_id: int,
    amount: Decimal,
    currency: Currency,
    description: str | None,
    payment_day: int | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
) -> Income:
    _validate(payment_day, start_date, end_date)
    return create_income(
        db,
        user_id=user_id,
        amount=amount,
        currency=currency,
        description=description,
        payment_day=payment_day,
        start_date=start_date,
        end_date=end_date,
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
    start_date: date | None = None,
    end_date: date | None = None,
) -> Income:
    income = get_income(db, user_id, income_id)
    if not income:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Renda não encontrada")
    _validate(payment_day, start_date, end_date)
    return update_income(
        db,
        income,
        amount=amount,
        currency=currency,
        description=description,
        payment_day=payment_day,
        start_date=start_date,
        end_date=end_date,
    )


def remove_income(db: Session, user_id: int, income_id: int) -> None:
    income = get_income(db, user_id, income_id)
    if not income:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Renda não encontrada")
    delete_income(db, income)


def total_monthly_income_brl(db: Session, user_id: int, year: int, month: int) -> Decimal:
    period_start, period_end = month_range(year, month)
    incomes = list_incomes_by_user(db, user_id)
    total = Decimal("0")
    for income in incomes:
        # income is active if it has no bounds, or its period overlaps with the requested month
        if income.start_date and income.start_date > period_end:
            continue
        if income.end_date and income.end_date < period_start:
            continue
        total += to_brl(income.amount, income.currency)
    return total
