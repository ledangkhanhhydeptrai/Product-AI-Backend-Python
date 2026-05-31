from datetime import datetime

from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

from sqlalchemy.dialects.postgresql import UUID


class Category(Base):
    __tablename__ = "categories"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    name = Column(String, nullable=False)

    description = Column(String)

    slug = Column(String)
    products = relationship(
        "Product",
        back_populates="category"
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
