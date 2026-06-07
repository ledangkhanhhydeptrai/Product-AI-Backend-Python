from uuid import UUID

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from app.core.security import verify_access_token

security = HTTPBearer()
optional_security = HTTPBearer(auto_error=False)


class CurrentUser(BaseModel):
    id: UUID
    role: str


def get_current_user(
        request: Request,
        credentials=Depends(security)
):
    token = None

    # 1. ưu tiên cookie
    if request.cookies.get("access_token"):
        token = request.cookies.get("access_token")

    # 2. fallback header
    elif credentials:
        token = credentials.credentials

    if not token:
        raise HTTPException(401, "Not authenticated")

    payload = verify_access_token(token)

    return CurrentUser(
        id=payload.get("sub"),
        role=payload.get("role")
    )


def get_optional_current_user(
        credentials: HTTPAuthorizationCredentials | None = Depends(optional_security)
):
    if credentials is None:
        return None

    try:
        token = credentials.credentials
        payload = verify_access_token(token)

        user_id = payload.get("sub")
        role = payload.get("role")

        if not user_id:
            return None

        return CurrentUser(
            id=user_id,
            role=role
        )
    except Exception:
        return None
