from fastapi import Depends, HTTPException

from app.core.deps import get_current_user
from app.core.enums import Role


def require_role(role: Role):
    def wrapper(user = Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return wrapper