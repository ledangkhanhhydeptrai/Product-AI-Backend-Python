from enum import Enum


class PaymentMethod(str, Enum):
    PAYOS = "PAYOS"
    COD = "COD"