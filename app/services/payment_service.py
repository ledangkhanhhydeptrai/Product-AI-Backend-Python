import time
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.payment import Payment
from app.enum.payment_method_status import PaymentMethod
from app.enum.payment_status import PaymentStatus
from app.services.pay_os_service import PayOSService


class PaymentService:

    @staticmethod
    def create_payment(db: Session, order_id: UUID, payment_method: PaymentMethod):

        order = db.query(Order).filter(Order.id == order_id).first()

        if not order:
            raise HTTPException(404, "Order not found")

        # ⚠️ FIX: auto generate nếu thiếu
        if not order.payos_order_code:
            order.payos_order_code = int(time.time() * 1000)
            db.commit()
            db.refresh(order)

        payment = Payment(
            order_id=order.id,
            amount=order.total_price,
            payment_method=payment_method,
            status=PaymentStatus.UNPAID
        )

        db.add(payment)
        db.commit()
        db.refresh(payment)

        # PAYOS FLOW
        if payment_method == PaymentMethod.PAYOS:
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
    def payment_success(db: Session, payment_id: UUID, transaction_id: str):

        payment = db.query(Payment).filter(Payment.id == payment_id).first()

        if not payment:
            raise HTTPException(404, "Payment not found")

        payment.status = PaymentStatus.PAID
        payment.transaction_id = transaction_id

        db.commit()
        db.refresh(payment)

        return payment

    @staticmethod
    def payment_failed(db: Session, payment_id: UUID):

        payment = db.query(Payment).filter(Payment.id == payment_id).first()

        if not payment:
            raise HTTPException(404, "Payment not found")

        payment.status = PaymentStatus.FAILED

        db.commit()
        db.refresh(payment)

        return payment
