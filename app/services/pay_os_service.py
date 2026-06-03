from payos import PayOS
from payos.type import PaymentData
from fastapi import HTTPException

from app.core.config import settings


class PayOSService:
    payos = PayOS(
        client_id=settings.PAYOS_CLIENT_ID,
        api_key=settings.PAYOS_API_KEY,
        checksum_key=settings.PAYOS_CHECKSUM_KEY
    )

    @staticmethod
    def create_link(order_code: int, amount: int, description: str):

        try:
            payment_data = PaymentData(
                orderCode=order_code,
                amount=amount,
                description=description,
                cancelUrl="http://localhost:3000/payment/cancel",
                returnUrl="http://localhost:3000/payment/success"
            )

            res = PayOSService.payos.createPaymentLink(payment_data)

            return res.checkoutUrl

        except Exception as e:
            raise HTTPException(500, str(e))
