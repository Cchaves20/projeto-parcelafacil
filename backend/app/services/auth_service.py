from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user_model import User
from app.repositories.user_repository import create_user, get_user_by_email, get_user_by_id
from app.utils.security import create_access_token, decode_access_token, hash_password, verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def register_user(db: Session, name: str, email: str, password: str) -> User:
    if get_user_by_email(db, email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="E-mail já cadastrado")
    return create_user(db, name=name, email=email, hashed_password=hash_password(password))


def authenticate_user(db: Session, email: str, password: str) -> str:
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    return create_access_token(subject=str(user.id))


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    user_id = decode_access_token(token)
    user = get_user_by_id(db, int(user_id)) if user_id else None
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
