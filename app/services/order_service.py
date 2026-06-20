import time
import random
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.cart import Cart
from app.enum.order_status import OrderStatus
from app.enum.payment_status import PaymentStatus
from app.schemas.order_schema import BuyNowRequest, CreateOrderFromCartRequest
from app.models.cart_item import CartItem
from app.schemas.order_schema import UpdateOrderRequest


def generate_order_code():
    return int(time.time() * 1000) + random.randint(100, 999)


class OrderService:

    @staticmethod
    def get_all_order(db: Session, user_id: UUID):
        return (
            db.query(Order)
            .options(
                joinedload(Order.order_items),
                joinedload(Order.payment)
            )
            .filter(Order.user_id == user_id)
            .all()
        )

    @staticmethod
    def buy_now(db: Session, request: BuyNowRequest, user_id: UUID):

        product = db.query(Product).filter(Product.id == request.product_id).first()

        if not product:
            raise HTTPException(404, "Product not found")

        total_price = product.price * request.quantity

        order = Order(
            user_id=user_id,
            shipping_address=request.shipping_address,
            payment_method=request.payment_method,
            payment_status=PaymentStatus.UNPAID,
            status=OrderStatus.PENDING,
            total_price=total_price,
            payos_order_code=generate_order_code()
        )

        db.add(order)
        db.commit()
        db.refresh(order)

        db.add(OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=request.quantity,
            price=product.price,
            subtotal=total_price
        ))

        db.commit()
        return order

    @staticmethod
    def create_order_by_user(db: Session, request: CreateOrderFromCartRequest, user_id: UUID):

        cart_items = (db.query(CartItem)
                      .join(Cart, Cart.id == CartItem.cart_id)
                      .filter(Cart.user_id == user_id, CartItem.id.in_(
            request.cart_item_ids))
                      .all())

        if not cart_items:
            raise HTTPException(400, "No cart items selected")

        total_price = sum(
            item.price * item.quantity for item in cart_items
        )

        order = Order(
            user_id=user_id,
            shipping_address=request.shipping_address,
            payment_method=request.payment_method,
            payment_status=PaymentStatus.UNPAID,
            status=OrderStatus.PENDING,
            total_price=total_price,
            payos_order_code=generate_order_code()
        )

        db.add(order)
        db.flush()

        items = [
            OrderItem(
                order_id=order.id,
                product_id=i.product_id,
                quantity=i.quantity,
                price=i.price,
                subtotal=i.price * i.quantity
            )
            for i in cart_items
        ]

        db.add_all(items)

        db.commit()
        db.refresh(order)

        return order

    @staticmethod
    def update_order_by_admin(db: Session, request: UpdateOrderRequest):

        # 1. Get order
        order = (
            db.query(Order)
            .filter(Order.id == request.order_id)
            .first()
        )

        if not order:
            raise HTTPException(
                status_code=404,
                detail="Order not found"
            )

        # 2. Không cho sửa đơn đã huỷ hoặc giao xong (tuỳ rule)
        if order.status in [OrderStatus.DELIVERED, OrderStatus.CANCELLED]:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot update order with status {order.status}"
            )

        # 3. Validate status transition
        VALID_TRANSITIONS = {
            OrderStatus.PENDING: [OrderStatus.PROCESSING, OrderStatus.CANCELLED],
            OrderStatus.PROCESSING: [OrderStatus.SHIPPED, OrderStatus.CANCELLED],
            OrderStatus.SHIPPED: [OrderStatus.DELIVERED],
        }

        # 4. Update status (nếu có)
        if request.status is not None:
            if request.status == order.status:
                return order  # 👈 cho phép giữ nguyên trạng thái
            allowed = VALID_TRANSITIONS.get(order.status, [])

            if request.status not in allowed:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid status transition: {order.status} -> {request.status}"
                )

            order.status = request.status

        # 5. Update payment status (nếu có)
        if request.payment_status is not None:
            order.payment_status = request.payment_status

        # 6. Update payment method (nếu có)
        if request.payment_method is not None:
            order.payment_method = request.payment_method

        # 7. Update shipping address (nếu có)
        if request.shipping_address is not None:
            order.shipping_address = request.shipping_address

        # 8. Commit
        db.commit()
        db.refresh(order)

        return order
