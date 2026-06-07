from fastapi import APIRouter, Depends, UploadFile, File, Form, Response
from sqlalchemy.orm import Session

from app.getDatabase.getAllDatabase import get_db
from app.schemas.auth_schema import RegisterRequest, LoginRequest
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/api",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)


@router.post("/auth/register", summary="")
def register(fullname: str = Form(...),
             email: str = Form(...),
             password: str = Form(...),
             phone: str = Form(...),
             db: Session = Depends(get_db),
             file: UploadFile = File(...)):
    request = RegisterRequest(
        fullName=fullname,
        email=email,
        password=password,
        phone=phone,
    )
    return AuthService.register(db, request, file)


@router.post("/auth/login", summary="")
def login(request: LoginRequest, response: Response, db: Session = Depends(get_db)):
    return AuthService.login(
        db=db,
        request=request,
        response=response
    )
