from fastapi import Depends, HTTPException, status

from app.core.deps import get_current_user
from app.core.enums import Role


def require_admin(user=Depends(get_current_user)):
    role = Role(user["role"])

    if role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin only"
        )

    return user


def require_staff(user=Depends(get_current_user)):
    role = Role(user["role"])
    if role not in [Role.ADMIN, Role.STAFF]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Staff or Admin only"
        )
    return user
