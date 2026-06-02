import uuid
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Brand(Base):
    __tablename__ = "brands"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    logo = Column(String)
    description = Column(String)
    products = relationship("Product", back_populates="brand")
