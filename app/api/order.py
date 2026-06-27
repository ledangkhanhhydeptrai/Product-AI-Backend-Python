from typing import List

from fastapi import APIRouter, Depends, Form, Path
from sqlalchemy.orm import Session
from uuid import UUID

from app.getDatabase.getAllDatabase import get_db

from app.response.ApiResponse import ApiResponse
from app.schemas.order_schema import OrderResponse, BuyNowRequest, CreateOrderFromCartRequest
from app.services.order_service import OrderService
from app.core.deps import get_current_user

from app.schemas.order_schema import UpdateOrderRequest
from app.core.permissions import require_admin
from app.enum.payment_method_status import PaymentMethod
from app.core.dependencies import require_role
from app.core.enums import Role

router = APIRouter(
    prefix="/api",
    tags=["Order"],
    responses={404: {"description": "Not found"}},
)


@router.get("/order", response_model=ApiResponse[list[OrderResponse]])
def get_all_order(user=Depends(get_current_user), db: Session = Depends(get_db)):
    order = OrderService.get_all_order(db, user.id)
    return {
        "status": 200,
        "message": "Get All Order Successfully",
        "data": order
    }


@router.post("/order/cart", response_model=ApiResponse[OrderResponse])
def create_order_from_cart(
        request: CreateOrderFromCartRequest,
        user=Depends(get_current_user),
        db: Session = Depends(get_db)
):
    order = OrderService.create_order_by_user(db=db, user_id=user.id, request=request)
    return {
        "status": 201,
        "message": "Create Order Successfully",
        "data": order
    }


@router.post("/order/buy-now", response_model=ApiResponse[OrderResponse])
def buy_now(
        product_id: UUID = Form(...),
        quantity: int = Form(...),
        shipping_address: str = Form(...),
        payment_method: PaymentMethod = Form(...),
        user=Depends(get_current_user),
        db: Session = Depends(get_db)
):
    request = BuyNowRequest(
        product_id=product_id,
        quantity=quantity,
        shipping_address=shipping_address,
        payment_method=payment_method
    )

    order = OrderService.buy_now(
        db=db,
        user_id=user.id,
        request=request
    )

    return {
        "status": 201,
        "message": "Buy Now Successfully",
        "data": order
    }


@router.put(
    "/admin/order/{id}",
    response_model=ApiResponse[OrderResponse],
    dependencies=[Depends(require_admin)],
)
def update_order_by_admin(
        request: UpdateOrderRequest,
        id: UUID = Path(...),
        db: Session = Depends(get_db),
):
    order = OrderService.update_order_by_admin(
        db=db,
        request=request,
        id=id
    )

    return {
        "status": 200,
        "message": "Order updated successfully",
        "data": order
    }


@router.get(
    "/admin/orders",
    dependencies=[Depends(require_role(Role.ADMIN))]
)
def get_all_orders(db: Session = Depends(get_db)):
    orderAdmin = OrderService.get_all_orders_admin(db)
    return {
        "status": 200,
        "message": "Get All Orders Successfully",
        "data": orderAdmin
    }
