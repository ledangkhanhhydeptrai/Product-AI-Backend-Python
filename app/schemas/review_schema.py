from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ReviewResponse(BaseModel):
    id: UUID
    user_id: UUID
    product_id: UUID
    rating: float
    comment: str
    created_at: datetime
    model_config = {
        "from_attributes": True
    }


class CreateReviewRequest(BaseModel):
    product_id: UUID
    rating: float
    comment: str
