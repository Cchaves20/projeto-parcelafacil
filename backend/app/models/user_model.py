from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    incomes = relationship("Income", back_populates="user", cascade="all, delete-orphan")
    categories = relationship("Category", back_populates="user", cascade="all, delete-orphan")
    recurring_expenses = relationship("RecurringExpense", back_populates="user", cascade="all, delete-orphan")
    installment_purchases = relationship("InstallmentPurchase", back_populates="user", cascade="all, delete-orphan")
    monthly_budgets = relationship("MonthlyBudget", back_populates="user", cascade="all, delete-orphan")
    sporadic_expenses = relationship("SporadicExpense", back_populates="user", cascade="all, delete-orphan")
    savings_boxes = relationship("SavingsBox", back_populates="user", cascade="all, delete-orphan")
