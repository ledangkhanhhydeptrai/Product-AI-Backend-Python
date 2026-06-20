import enum

class OrderStatus(str, enum.Enum):
    PROCESSING = "PROCESSING"
    PENDING = "PENDING"
    PAID = "PAID"
    SHIPPED = "SHIPPED"   # 👈 FIX
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"