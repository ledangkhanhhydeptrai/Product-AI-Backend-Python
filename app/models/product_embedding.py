import uuid

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class ProductEmbedding(Base):
    __tablename__ = "product_embeddings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.id"),
        unique=True
    )
    product = relationship("Product", back_populates="product_embedding")

    embedding = Column(Vector(768))
