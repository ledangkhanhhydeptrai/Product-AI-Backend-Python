from sqlalchemy import Column, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    order_id = Column(
        UUID(as_uuid=True),
        ForeignKey("orders.id")
    )

    product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.id")
    )

    quantity = Column(Integer, default=1)

    price = Column(Float, nullable=False)

    subtotal = Column(Float, nullable=False)

    order = relationship(
        "Order",
        back_populates="order_items"
    )

    product = relationship(
        "Product",
        back_populates="order_items"
    )
