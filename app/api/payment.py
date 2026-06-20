from uuid import UUID

from fastapi import APIRouter, Depends, Form

from sqlalchemy.orm import Session

from app.getDatabase.getAllDatabase import get_db
from app.services.payment_service import PaymentService

from app.response.ApiResponse import ApiResponse
from app.schemas.payment_schemas import PaymentResponse
from app.core.enums import Role
from app.core.dependencies import require_role

router = APIRouter(prefix="/api", tags=["Payment"])


@router.put("/payment-callback/success/{order_code}", response_model=ApiResponse[PaymentResponse],
            dependencies=[Depends(require_role(Role.USER))])
def payment_success(
        order_code: int, db: Session = Depends(get_db),
):
    payment = PaymentService.payment_success(db, order_code)
    return {
        "status": 200,
        "message": "Success Payment Successfully",
        "data": payment
    }


@router.put(
    "/payment-callback/failed/{order_code}",
    response_model=ApiResponse[PaymentResponse],
    dependencies=[Depends(require_role(Role.USER))]
)
def payment_failed(
        order_code: int,
        db: Session = Depends(get_db)
):
    payment = PaymentService.payment_failed(
        db,
        order_code
    )

    return {
        "status": 200,
        "message": "Payment Failed",
        "data": payment
    }


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
        db: Session = Depends(get_db)
):
    payment = PaymentService.create_payment(
        db=db,
        order_id=order_id,
    )

    return {
        "status": 201,
        "message": "Create Payment Successfully",
        "data": payment
    }
