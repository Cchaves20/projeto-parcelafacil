from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user_model import User
from app.services.auth_service import get_current_user
from app.services.calendar_service import get_due_items

router = APIRouter(prefix="/calendar", tags=["calendar"])


@router.get("")
def get_calendar(
    start_date: date = Query(...),
    end_date: date = Query(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_due_items(db, current_user.id, start_date, end_date)
