from uuid import UUID

from fastapi import APIRouter, Depends, Form

from sqlalchemy.orm import Session

from app.getDatabase.getAllDatabase import get_db
from app.services.payment_service import PaymentService

from app.response.ApiResponse import ApiResponse
from app.enum.payment_method_status import PaymentMethod
from app.schemas.payment_schemas import PaymentResponse
from app.core.enums import Role
from app.core.dependencies import require_role

router = APIRouter(prefix="/api", tags=["Payment"])


@router.get("/payment/{order_id}", response_model=ApiResponse[PaymentResponse],
            dependencies=[Depends(require_role(Role.USER))])
def get_payment(order_id: UUID, db: Session = Depends(get_db), ):
    payment = PaymentService.get_payment_by_order_id(db=db, order_id=order_id)
    return {
        "status": 200,
        "message": "Get payment successfully",
        "data": payment
    }


@router.post("/payment/{order_id}", response_model=ApiResponse[PaymentResponse],
             dependencies=[Depends(require_role(Role.USER))])
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


@router.post("/payment/success/{payment_id}/{transaction_id}", response_model=ApiResponse[PaymentResponse],
             dependencies=[Depends(require_role(Role.USER))])
def payment_success(
        payment_id: UUID, transaction_id: str, db: Session = Depends(get_db),
):
    payment = PaymentService.payment_success(db, payment_id, transaction_id)
    return {
        "status": 200,
        "message": "Success Payment Successfully",
        "data": payment
    }


@router.post(
    "/payment/failed/{payment_id}",
    response_model=ApiResponse[PaymentResponse],
    dependencies=[Depends(require_role(Role.USER))]
)
def payment_failed(
        payment_id: UUID,
        db: Session = Depends(get_db),
):
    payment = PaymentService.payment_failed(db, payment_id)

    return {
        "status": 200,
        "message": "Payment Failed",
        "data": payment
    }
