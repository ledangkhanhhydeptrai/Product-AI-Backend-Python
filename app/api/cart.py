from uuid import UUID

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from app.response.ApiResponse import ApiResponse
from app.schemas.cart_schema import CartResponse, AddCartRequest, UpdateCartRequest, UpdateCartItemResponse
from app.services.cart_service import CartService
from app.getDatabase.getAllDatabase import get_db
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/api",
    tags=["Carts"],
    responses={404: {"description": "Not found"}},
)


@router.get("/cart", response_model=ApiResponse[list[CartResponse]])
def get_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart = CartService.get_cart(db, current_user.id)
    return {
        "status": 200,
        "message": "Get All Cart Successfully",
        "data": cart
    }


@router.post("/cart/items", response_model=ApiResponse[CartResponse])
def add_to_cart(
        request: AddCartRequest,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    result = CartService.add_to_cart(
        db=db,
        user_id=user.id,
        product_id=request.product_id,
        quantity=request.quantity
    )

    return {
        "status": 200,
        "message": "Added to cart successfully",
        "data": result
    }


from uuid import UUID


@router.put("/cart/product/{product_id}", response_model=ApiResponse[CartResponse])
def update_cart(
        product_id: UUID,
        request: UpdateCartRequest,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    result = CartService.update_quantity(
        db=db,
        user_id=user.id,
        product_id=product_id,
        quantity=request.quantity
    )

    return {
        "status": 200,
        "message": "Update Successfully",
        "data": result
    }


@router.delete("/cart/{cart_item_id}")
def delete_cart(db: Session = Depends(get_db), user: User = Depends(get_current_user), cart_item_id: UUID = Path(...)):
    CartService.remove_item(db=db, user_id=user.id, cart_item_id=cart_item_id)
    return {
        "status": 200,
        "message": "Deleted Successfully",
        "data": None
    }
