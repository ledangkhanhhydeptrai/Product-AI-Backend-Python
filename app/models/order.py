from datetime import datetime

from sqlalchemy import Column, ForeignKey, Float, String, Enum, DateTime, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid

from app.enum.order_status import OrderStatus
from app.enum.payment_method_status import PaymentMethod
from app.enum.payment_status import PaymentStatus


class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    total_price = Column(Float, nullable=False)

    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)

    shipping_address = Column(String, nullable=False)

    payment_method = Column(Enum(PaymentMethod), nullable=False)

    payos_order_code = Column(BigInteger, unique=True, nullable=True)

    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.UNPAID)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    payment = relationship("Payment", back_populates="order", uselist=False)
    order_items = relationship("OrderItem", back_populates="order")
    # ⚠️ FIX: 1 order chỉ 1 payment
   