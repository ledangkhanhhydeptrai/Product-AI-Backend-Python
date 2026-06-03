from uuid import UUID

from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session

from app.getDatabase.getAllDatabase import get_db
from app.services.payment_service import PaymentService

from app.response.ApiResponse import ApiResponse
from app.enum.payment_method_status import PaymentMethod
from app.schemas.payment_schemas import PaymentResponse

router = APIRouter(prefix="/api", tags=["Payment"])


@router.post("/payment/{order_id}", response_model=ApiResponse[PaymentResponse])
def create_payment(
        order_id: UUID,
        payment_method: PaymentMethod = Form(...),
        db: Session = Depends(get_db)
):
    payment = PaymentService.create_payment(
        db=db,
        order_id=order_id,
        payment_method=payment_method
    )

    return {
        "status": 201,
        "message": "Create Payment Successfully",
        "data": payment
    }
