import time
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.payment import Payment

from app.enum.order_status import OrderStatus
from app.enum.payment_method_status import PaymentMethod
from app.enum.payment_status import PaymentStatus

from app.services.pay_os_service import PayOSService


class PaymentService:

    @staticmethod
    def get_payment_by_order_id(db: Session, order_id: UUID):
        return (
            db.query(Payment)
            .filter(Payment.order_id == order_id)
            .order_by(Payment.created_at.desc())
            .first()
        )

    @staticmethod
    def create_payment(
            db: Session,
            order_id: UUID,
    ):
        order = (
            db.query(Order)
            .filter(Order.id == order_id)
            .first()
        )

        if not order:
            raise HTTPException(
                status_code=404,
                detail="Order not found"
            )

        # Không tạo payment trùng
        existing_payment = (
            db.query(Payment)
            .filter(Payment.order_id == order_id)
            .first()
        )

        if existing_payment:
            return existing_payment

        if not order.payos_order_code:
            order.payos_order_code = int(time.time() * 1000)
            db.commit()
            db.refresh(order)

        payment = Payment(
            order_id=order.id,
            amount=order.total_price,
            status=PaymentStatus.UNPAID,
            payment_method=PaymentMethod.PAYOS,
        )

        db.add(payment)
        db.commit()
        db.refresh(payment)

        if order.payment_method == PaymentMethod.PAYOS:
            checkout_url = PayOSService.create_link(
                order_code=order.payos_order_code,
                amount=int(order.total_price),
                description=f"Order {order.payos_order_code}"
            )

            payment.checkout_url = checkout_url

            db.commit()
            db.refresh(payment)

        return payment

    @staticmethod
    def payment_success(
            db: Session,
            payment_id: UUID,
            transaction_id: str
    ):
        payment = (
            db.query(Payment)
            .filter(Payment.id == payment_id)
            .first()
        )

        if not payment:
            raise HTTPException(
                status_code=404,
                detail="Payment not found"
            )

        order = (
            db.query(Order)
            .filter(Order.id == payment.order_id)
            .first()
        )

        if not order:
            raise HTTPException(
                status_code=404,
                detail="Order not found"
            )

        payment.status = PaymentStatus.PAID
        payment.transaction_id = transaction_id

        order.payment_status = PaymentStatus.PAID
        order.status = OrderStatus.PROCESSING

        db.commit()
        db.refresh(payment)

        return payment

    @staticmethod
    def payment_failed(
            db: Session,
            payment_id: UUID
    ):
        payment = (
            db.query(Payment)
            .filter(Payment.id == payment_id)
            .first()
        )

        if not payment:
            raise HTTPException(
                status_code=404,
                detail="Payment not found"
            )

        order = (
            db.query(Order)
            .filter(Order.id == payment.order_id)
            .first()
        )

        if not order:
            raise HTTPException(
                status_code=404,
                detail="Order not found"
            )

        payment.status = PaymentStatus.FAILED

        order.payment_status = PaymentStatus.FAILED
        order.status = OrderStatus.CANCELLED

        db.commit()
        db.refresh(payment)

        return payment
