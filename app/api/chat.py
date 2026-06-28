from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.response.ApiResponse import ApiResponse

from app.schemas.chat_schema import ChatRequest, AIResponse
from app.getDatabase.getAllDatabase import get_db

from app.services.chat_service import ChatService
from app.core.deps import CurrentUser, get_optional_current_user

router = APIRouter(
    prefix="/api",
    tags=["Chat"],
    responses={404: {"description": "Not found"}},
)


@router.get("/chat", response_model=ApiResponse[list[AIResponse]])
def get_all_chat(db: Session = Depends(get_db)):
    chat = ChatService.get_all_chat(db)
    return {
        "status": 200,
        "message": "Get all chat Successfully",
        "data": chat
    }


@router.post("/chat/create", response_model=ApiResponse)
def chat(
        req: ChatRequest,
        current_user: CurrentUser | None = Depends(get_optional_current_user),
        db: Session = Depends(get_db)
):
    user_id = current_user.id if current_user else None

    result = ChatService.chat(
        db=db,
        req=req,
        user_id=user_id
    )

    return ApiResponse(
        status=200,
        message="Success",
        data=result
    )
