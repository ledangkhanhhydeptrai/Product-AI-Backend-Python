from typing import Optional

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID


class AIResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: Optional[UUID] = None
    role: str
    content: str
    created_at: datetime


class ChatRequest(BaseModel):
    message: str
    model_config = {
        "from_attributes": True
    }
