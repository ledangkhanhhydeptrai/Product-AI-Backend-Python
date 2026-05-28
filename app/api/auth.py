from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.schemas.auth_schema import RegisterRequest, LoginRequest
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    return AuthService.register(db, request)


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    return AuthService.login(db, request)
