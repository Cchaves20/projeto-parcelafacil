from sqlalchemy.orm import Session

from app.models.category_model import Category


def create_category(db: Session, user_id: int, name: str) -> Category:
    category = Category(user_id=user_id, name=name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def list_categories_by_user(db: Session, user_id: int) -> list[Category]:
    return db.query(Category).filter(Category.user_id == user_id).all()


def get_category(db: Session, user_id: int, category_id: int) -> Category | None:
    return db.query(Category).filter(Category.user_id == user_id, Category.id == category_id).first()


def delete_category(db: Session, category: Category) -> None:
    db.delete(category)
    db.commit()
