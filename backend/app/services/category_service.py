from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.category_model import Category
from app.repositories.category_repository import (
    create_category,
    delete_category,
    get_category,
    list_categories_by_user,
)


def add_category(db: Session, user_id: int, name: str) -> Category:
    return create_category(db, user_id=user_id, name=name)


def list_categories(db: Session, user_id: int) -> list[Category]:
    return list_categories_by_user(db, user_id)


def remove_category(db: Session, user_id: int, category_id: int) -> None:
    category = get_category(db, user_id, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada")
    delete_category(db, category)
