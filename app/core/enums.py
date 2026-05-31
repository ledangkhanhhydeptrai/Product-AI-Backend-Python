import enum

class Role(str, enum.Enum):
    ADMIN = "admin"
    STAFF = "staff"
    USER = "user"