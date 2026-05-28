from typing import TypeVar, Optional, Generic

from pydantic import BaseModel

T = TypeVar('T')

class ApiResponse(BaseModel, Generic[T]):
    status: int
    message: str
    data: Optional[T] = None
