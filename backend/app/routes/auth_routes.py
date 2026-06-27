from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth_schema import LoginRequest, Token
from app.schemas.user_schema import UserCreate, UserRead
from app.services.auth_service import authenticate_user, register_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, name=payload.name, email=payload.email, password=payload.password)


@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    access_token = authenticate_user(db, email=payload.email, password=payload.password)
    return Token(access_token=access_token)
