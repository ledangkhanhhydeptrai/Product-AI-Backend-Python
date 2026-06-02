from datetime import datetime

from sqlalchemy import Column, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid


class Cart(Base):
    __tablename__ = "carts"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    created_at = Column(DateTime, server_default=func.now())
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id")
    )

    user = relationship(
        "User"
    )

    cart_items = relationship(
        "CartItem",
        back_populates="cart",
        cascade="all, delete-orphan"
    )
