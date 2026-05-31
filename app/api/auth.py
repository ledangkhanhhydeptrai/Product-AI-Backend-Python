from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.getDatabase.getAllDatabase import get_db
from app.schemas.auth_schema import RegisterRequest, LoginRequest
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)


@router.post("/register", summary="")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    return AuthService.register(db, request)


@router.post("/login", summary="")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    return AuthService.login(db, request)
