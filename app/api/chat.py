from fastapi import APIRouter

from app.response.ApiResponse import ApiResponse
from app.services.ollama_service import chat_with_ai
from app.schemas.chat_schema import ChatRequest

router = APIRouter()


@router.post("/chat", response_model=ApiResponse)
def chat(req: ChatRequest):
    response = chat_with_ai(req.message)
    return ApiResponse(
        status=200,
        message="Trả kết quả thành công",
        data=response
    )
