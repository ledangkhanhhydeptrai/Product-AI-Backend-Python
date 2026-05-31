from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.security import verify_password, create_access_token, hash_password
from app.models.user import User
from app.response.ApiResponse import ApiResponse


class AuthService:
    @staticmethod
    def register(db: Session, request):
        existing_user = (db.query(User).
                         filter(User.email == request.email)
                         .first())
        if existing_user:
            raise HTTPException(status_code=400,
                                detail="Email already registered")
        hashed_password = hash_password(request.password)
        user = User(
            full_name=request.fullName,
            email=request.email,
            password=hashed_password
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return ApiResponse(
            status=200,
            message="User created successfully"
        )

    @staticmethod
    def login(db: Session, request):
        user = db.query(User).filter(User.email == request.email).first()
        if not user:
            raise HTTPException(status_code=400, detail="Invalid credentials")
        valid_password = verify_password(request.password, user.password)
        if not valid_password:
            raise HTTPException(status_code=400,
                                detail="Invalid credentials")
        token = create_access_token({"sub": str(user.id)})
        return ApiResponse(
            status=200,
            message="User login successfully",
            data={
                "token": token,
                "role": user.role
            }
        )
