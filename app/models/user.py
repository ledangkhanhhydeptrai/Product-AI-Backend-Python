import uuid

from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    phone = Column(String)
    avatar = Column(String)
    role = Column(String, default="USER")
    is_active = Column(Boolean, default=True)
    orders = relationship("Order",
                          back_populates="user",
                          cascade="all,delete-orphan")

    reviews = relationship(
        "Review",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    ai_chat_histories = relationship(
        "AIChatHistory",
        back_populates="user",
        cascade="all, delete-orphan"
    )
