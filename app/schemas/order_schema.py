from datetime import datetime

from uuid import UUID

from pydantic import BaseModel

from app.enum.payment_method_status import PaymentMethod


class OrderItem(BaseModel):
    id: UUID
    order_id: UUID
    product_id: UUID
    quantity: int
    price: float
    subtotal: float
    model_config = {
        "from_attributes": True
    }


class OrderResponse(BaseModel):
    id: UUID
    status: str
    total_price: float
    shipping_address: str
    payment_method: str
    created_at: datetime

    order_items: list[OrderItem]  # ✅ FIX

    model_config = {"from_attributes": True}


class CreateOrderFromCartRequest(BaseModel):
    shipping_address: str
    payment_method: PaymentMethod


class BuyNowRequest(BaseModel):
    product_id: UUID
    quantity: int
    shipping_address: str
    payment_method: PaymentMethod
