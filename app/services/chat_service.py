from uuid import UUID

from sqlalchemy import asc
from sqlalchemy.orm import Session

from app.models.ai_chat_histories import AIChatHistory
from app.schemas.chat_schema import ChatRequest
from app.services.ollama_service import chat_with_ai


class ChatService:
    @staticmethod
    def get_all_chat(db: Session):
        return db.query(AIChatHistory).order_by(asc(AIChatHistory.id)).all()

    @staticmethod
    def chat(db: Session, req: ChatRequest, user_id: UUID):
        answer = chat_with_ai(req.message)

        user_message = AIChatHistory(
            user_id=user_id,
            role="user",
            content=req.message
        )

        assistant_message = AIChatHistory(
            user_id=user_id,
            role="assistant",
            content=answer
        )

        db.add(user_message)
        db.add(assistant_message)

        db.commit()

        return {
            "message": req.message,
            "response": answer
        }
