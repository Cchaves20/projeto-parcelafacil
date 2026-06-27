from sqlalchemy import Boolean, Column, Date, Enum, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.enums import InstallmentStatus


class Installment(Base):
    __tablename__ = "installments"

    id = Column(Integer, primary_key=True, index=True)
    purchase_id = Column(Integer, ForeignKey("installment_purchases.id"), nullable=False, index=True)
    number = Column(Integer, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    due_date = Column(Date, nullable=False, index=True)
    status = Column(Enum(InstallmentStatus), nullable=False, default=InstallmentStatus.PENDING)

    purchase = relationship("InstallmentPurchase", back_populates="installments")
