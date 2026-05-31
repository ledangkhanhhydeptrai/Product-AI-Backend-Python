from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    fullName: str
    email: EmailStr
    password: str
    phone: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
