from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.enums import Currency


class Income(Base):
    __tablename__ = "incomes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    description = Column(String(150), nullable=True)
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(Enum(Currency), nullable=False, default=Currency.BRL)
    payment_day = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="incomes")
