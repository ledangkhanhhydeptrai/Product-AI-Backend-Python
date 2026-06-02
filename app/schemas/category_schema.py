from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CategoryResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    description: str
    created_at: datetime
    model_config = {
        "from_attributes": True
    }


class CategoryCreateRequest(BaseModel):
    name: str
    slug: str
    description: str
