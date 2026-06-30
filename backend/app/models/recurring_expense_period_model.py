from sqlalchemy import Column, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database import Base


class RecurringExpensePeriod(Base):
    __tablename__ = "recurring_expense_periods"

    id = Column(Integer, primary_key=True, index=True)
    recurring_expense_id = Column(Integer, ForeignKey("recurring_expenses.id"), nullable=False, index=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)

    recurring_expense = relationship("RecurringExpense", back_populates="periods")
