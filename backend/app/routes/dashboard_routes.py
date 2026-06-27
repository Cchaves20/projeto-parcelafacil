from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user_model import User
from app.schemas.dashboard_schema import MonthlySummary
from app.services.auth_service import get_current_user
from app.services.dashboard_service import get_monthly_summary

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=MonthlySummary)
def get_summary(
    year: int = Query(default_factory=lambda: date.today().year),
    month: int = Query(default_factory=lambda: date.today().month, ge=1, le=12),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_monthly_summary(db, current_user.id, year, month)
