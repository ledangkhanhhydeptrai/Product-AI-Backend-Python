from fastapi import APIRouter
from app.services.ollama_service import chat_with_ai
from app.schemas.chat_schema import ChatRequest

router = APIRouter()

@router.post("/chat")
def chat(req: ChatRequest):
    response = chat_with_ai(req.message)
    return {"AI": response}