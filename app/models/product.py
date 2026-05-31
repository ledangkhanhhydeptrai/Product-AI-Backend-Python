from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid

from app.models.brand import Brand
from app.models.category import Category
from app.models.cart_item import CartItem
from app.models.order_item import OrderItem
from app.models.review import Review


class Product(Base):
    __tablename__ = "products"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    name = Column(String, nullable=False)

    description = Column(String)

    price = Column(Float, nullable=False)

    stock = Column(Integer, default=0)

    image_url = Column(String)

    category_id = Column(
        UUID(as_uuid=True),
        ForeignKey("categories.id")
    )

    category = relationship(
        "Category",
        back_populates="products"
    )
    brand_id = Column(
        UUID(as_uuid=True),
        ForeignKey("brands.id")
    )
    brand = relationship(
        "Brand",
        back_populates="products"
    )
    cart_items = relationship(
        "CartItem",
        back_populates="product"
    )

    order_items = relationship(
        "OrderItem",
        back_populates="product"
    )

    reviews = relationship(
        "Review",
        back_populates="product"
    )
