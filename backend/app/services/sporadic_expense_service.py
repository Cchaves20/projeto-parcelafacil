from datetime import date
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.enums import Currency
from app.models.sporadic_expense_model import SporadicExpense
from app.repositories.sporadic_expense_repository import (
    create_sporadic_expense,
    delete_sporadic_expense,
    get_sporadic_expense,
    list_sporadic_expenses_by_user,
)


def add_sporadic_expense(
    db: Session,
    user_id: int,
    description: str,
    amount: Decimal,
    currency: Currency,
    expense_date: date,
    category_id: int | None,
) -> SporadicExpense:
    expense = SporadicExpense(
        user_id=user_id,
        description=description,
        amount=amount,
        currency=currency,
        expense_date=expense_date,
        category_id=category_id,
    )
    return create_sporadic_expense(db, expense)


def list_sporadic_expenses(db: Session, user_id: int) -> list[SporadicExpense]:
    return list_sporadic_expenses_by_user(db, user_id)


def edit_sporadic_expense(
    db: Session,
    user_id: int,
    expense_id: int,
    description: str,
    amount: Decimal,
    currency: Currency,
    expense_date: date,
    category_id: int | None,
) -> SporadicExpense:
    expense = get_sporadic_expense(db, user_id, expense_id)
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gasto esporádico não encontrado")
    expense.description = description
    expense.amount = amount
    expense.currency = currency
    expense.expense_date = expense_date
    expense.category_id = category_id
    db.commit()
    db.refresh(expense)
    return expense


def remove_sporadic_expense(db: Session, user_id: int, expense_id: int) -> None:
    expense = get_sporadic_expense(db, user_id, expense_id)
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gasto esporádico não encontrado")
    delete_sporadic_expense(db, expense)
