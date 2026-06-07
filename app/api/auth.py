from fastapi import APIRouter, Depends, UploadFile, File, Form, Response, Request, HTTPException
from sqlalchemy.orm import Session

from app.getDatabase.getAllDatabase import get_db
from app.schemas.auth_schema import RegisterRequest, LoginRequest
from app.services.auth_service import AuthService
from app.core.security import verify_access_token, create_access_token, verify_password
from app.models.user import User

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
    return AuthService.login(db, request, response)


@router.get("/debug/me")
def debug_me(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        return {
            "authenticated": False,
            "user": None
        }

    payload = verify_access_token(token)

    return {
        "authenticated": True,
        "user": payload
    }


@router.post("/auth/login-debug")
def login_debug(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(request.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({
        "sub": str(user.id),
        "role": user.role
    })

    return {
        "token": token,  # 👈 chỉ dùng để test Swagger
        "user": {
            "id": str(user.id),
            "role": user.role,
            "email": user.email
        }
    }
