from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False)

    user = relationship("User", back_populates="categories")
    recurring_expenses = relationship("RecurringExpense", back_populates="category")
    installment_purchases = relationship("InstallmentPurchase", back_populates="category")
    sporadic_expenses = relationship("SporadicExpense", back_populates="category")
