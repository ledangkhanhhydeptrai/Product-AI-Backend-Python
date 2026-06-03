import uuid
from sqlalchemy import Column, Float, String, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.enum.payment_status import PaymentStatus
from app.enum.payment_method_status import PaymentMethod


class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)

    amount = Column(Float, nullable=False)

    payment_method = Column(Enum(PaymentMethod), nullable=False)

    status = Column(Enum(PaymentStatus), default=PaymentStatus.UNPAID)

    transaction_id = Column(String, nullable=True)  # ⚠️ FIX STRING

    checkout_url = Column(String, nullable=True)

    order = relationship("Order", back_populates="payment")
