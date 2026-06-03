from enum import Enum


class PaymentStatus(str, Enum):
    UNPAID = "UNPAID"
    PAID = "PAID"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"