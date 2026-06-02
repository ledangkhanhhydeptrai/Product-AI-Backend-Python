from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid


class AIChatHistory(Base):
    __tablename__ = "ai_chat_histories"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id")
    )

    message = Column(String, nullable=False)

    response = Column(String, nullable=False)

    user = relationship(
        "User",
        back_populates="ai_chat_histories"
    )
