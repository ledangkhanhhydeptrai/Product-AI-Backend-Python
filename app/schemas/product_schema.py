from datetime import datetime

from pydantic import BaseModel


class ProductResponse(BaseModel):
    id: str
    name: str
    slug: str
    description: str
    price: float
    stock: int
    thumbnail: str
    category_id: str
    brand_id: str
    rating_average: float
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductCreateRequest(BaseModel):
    name: str
    slug: str
    description: str
    price: float
    stock: int
    thumbnail: str
    category_id: str
    brand_id: str
    is_active: bool = True
