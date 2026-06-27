from datetime import datetime
from typing import Optional

from uuid import UUID

from pydantic import BaseModel

from app.enum.payment_method_status import PaymentMethod
from app.enum.order_status import OrderStatus
from app.enum.payment_status import PaymentStatus


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
    cart_item_ids: list[UUID]
    shipping_address: str
    payment_method: PaymentMethod


class BuyNowRequest(BaseModel):
    product_id: UUID
    quantity: int
    shipping_address: str
    payment_method: PaymentMethod

class UpdateOrderRequest(BaseModel):
    status: Optional[OrderStatus] = None
    payment_status: Optional[PaymentStatus] = None
    payment_method: Optional[PaymentMethod] = None
    shipping_address: Optional[str] = None
