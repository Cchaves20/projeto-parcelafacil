from sqlalchemy import JSON, Boolean, Column, Enum, ForeignKey, Integer, Numeric, String, DateTime, func
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.enums import Currency, Frequency


class RecurringExpense(Base):
    __tablename__ = "recurring_expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True, index=True)
    name = Column(String(150), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(Enum(Currency), nullable=False, default=Currency.BRL)
    frequency = Column(Enum(Frequency), nullable=False, default=Frequency.MONTHLY)
    billing_day = Column(Integer, nullable=True)
    weekdays = Column(JSON, nullable=True)
    estimated_monthly_occurrences = Column(Integer, nullable=True)
    active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="recurring_expenses")
    category = relationship("Category", back_populates="recurring_expenses")
    periods = relationship(
        "RecurringExpensePeriod", back_populates="recurring_expense", cascade="all, delete-orphan"
    )
