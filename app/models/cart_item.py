from sqlalchemy import Column, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    price = Column(Float)
    cart_id = Column(
        UUID(as_uuid=True),
        ForeignKey("carts.id")
    )

    product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.id")
    )

    quantity = Column(Integer, default=1)

    cart = relationship(
        "Cart",
        back_populates="cart_items"
    )

    product = relationship(
        "Product",
        back_populates="cart_items"
    )
