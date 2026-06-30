from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.enums import Currency


class SavingsBox(Base):
    __tablename__ = "savings_boxes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(150), nullable=False)
    currency = Column(Enum(Currency), nullable=False, default=Currency.BRL)
    annual_rate = Column(Numeric(8, 4), nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="savings_boxes")
    transactions = relationship("SavingsTransaction", back_populates="box", cascade="all, delete-orphan")


class SavingsTransaction(Base):
    __tablename__ = "savings_transactions"

    id = Column(Integer, primary_key=True, index=True)
    box_id = Column(Integer, ForeignKey("savings_boxes.id"), nullable=False, index=True)
    amount = Column(Numeric(12, 2), nullable=False)
    description = Column(String(200), nullable=True)
    transaction_date = Column(DateTime(timezone=True), server_default=func.now())

    box = relationship("SavingsBox", back_populates="transactions")
