from sqlalchemy import Column, String
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

    products = relationship(
        "Product",
        back_populates="category"
    )
