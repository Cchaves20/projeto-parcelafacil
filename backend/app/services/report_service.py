from sqlalchemy.orm import Session

from app.schemas.dashboard_schema import MonthlySummary
from app.services.dashboard_service import get_monthly_summary


def get_annual_report(db: Session, user_id: int, year: int) -> list[MonthlySummary]:
    return [get_monthly_summary(db, user_id, year, month) for month in range(1, 13)]
