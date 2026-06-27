from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user_model import User
from app.schemas.dashboard_schema import MonthlySummary
from app.services.auth_service import get_current_user
from app.services.report_service import get_annual_report

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/annual", response_model=list[MonthlySummary])
def get_annual(
    year: int = Query(default_factory=lambda: date.today().year),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_annual_report(db, current_user.id, year)
