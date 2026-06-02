from fastapi import APIRouter

from app.response.ApiResponse import ApiResponse
from app.services.ollama_service import chat_with_ai
from app.schemas.chat_schema import ChatRequest

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=ApiResponse)
def chat(req: ChatRequest):
    response = chat_with_ai(req.message)
    return ApiResponse(
        status=200,
        message="Trả kết quả thành công",
        data=response
    )
