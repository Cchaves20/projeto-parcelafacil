from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user_model import User
from app.repositories.user_repository import create_user, get_user_by_email
from fastapi import Depends

DEFAULT_USER_EMAIL = "owner@parcelafacil.app"
DEFAULT_USER_NAME = "Eu"


def get_or_create_default_user(db: Session) -> User:
    user = get_user_by_email(db, DEFAULT_USER_EMAIL)
    if not user:
        user = create_user(db, name=DEFAULT_USER_NAME, email=DEFAULT_USER_EMAIL, hashed_password="")
    return user


def get_current_user(db: Session = Depends(get_db)) -> User:
    return get_or_create_default_user(db)
