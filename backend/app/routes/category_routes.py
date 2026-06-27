from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user_model import User
from app.schemas.category_schema import CategoryCreate, CategoryRead
from app.services.auth_service import get_current_user
from app.services.category_service import add_category, list_categories, remove_category

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(
    payload: CategoryCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return add_category(db, current_user.id, name=payload.name)


@router.get("", response_model=list[CategoryRead])
def get_categories(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return list_categories(db, current_user.id)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category_route(
    category_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    remove_category(db, current_user.id, category_id)
