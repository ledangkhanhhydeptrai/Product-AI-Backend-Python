from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from app.core.security import verify_access_token

security = HTTPBearer()


class CurrentUser(BaseModel):
    id: UUID
    role: str


def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security)
):
    print("Credentials:", credentials)
    token = credentials.credentials
    payload = verify_access_token(token)

    user_id = payload.get("sub")
    role = payload.get("role")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    return CurrentUser(
        id=user_id,
        role=role
    )
