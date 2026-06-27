from sqlalchemy import Column, Date, DateTime, Enum, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.enums import Currency


class InstallmentPurchase(Base):
    __tablename__ = "installment_purchases"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True, index=True)
    description = Column(String(150), nullable=False)
    total_amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(Enum(Currency), nullable=False, default=Currency.BRL)
    installments_count = Column(Integer, nullable=False)
    first_due_date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="installment_purchases")
    category = relationship("Category", back_populates="installment_purchases")
    installments = relationship(
        "Installment", back_populates="purchase", cascade="all, delete-orphan", order_by="Installment.number"
    )
