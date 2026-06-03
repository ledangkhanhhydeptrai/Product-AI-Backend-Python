from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.enum.payment_method_status import PaymentMethod
from app.enum.payment_status import PaymentStatus


class PaymentResponse(BaseModel):
    id: UUID
    amount: float
    payment_method: PaymentMethod
    status: str
    transaction_id: str | None
    checkout_url: str | None

    model_config = {"from_attributes": True}


class PaymentWebhookRequest(BaseModel):
    payment_id: UUID
    transaction_id: UUID


class CreatePaymentResponse(BaseModel):
    payment_id: UUID
    order_id: UUID
    status: PaymentStatus
    checkout_url: str | None = None
