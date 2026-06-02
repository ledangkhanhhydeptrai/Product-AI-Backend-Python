from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.models.cart_item import CartItem

class CartItemResponse(BaseModel):
    id: UUID
    product_id: UUID
    quantity: int
    price: float

    class Config:
        from_attributes = True
class CartResponse(BaseModel):
    id: UUID
    user_id: UUID
    created_at: datetime
    cart_items: list[CartItemResponse]

    class Config:
        from_attributes = True


class AddCartRequest(BaseModel):
    product_id: UUID
    quantity: int
