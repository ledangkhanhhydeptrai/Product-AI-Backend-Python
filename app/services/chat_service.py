import time
import re
from uuid import UUID
from sqlalchemy import asc
from sqlalchemy.orm import Session

from app.models.ai_chat_histories import AIChatHistory
from app.models.product import Product
from app.schemas.chat_schema import ChatRequest
from app.services.ollama_service import chat_with_ai


class ChatService:
    @staticmethod
    def get_all_chat(db: Session):
        return (
            db.query(AIChatHistory)
            .order_by(asc(AIChatHistory.created_at))
            .all()
        )

    @staticmethod
    def chat(db: Session, req: ChatRequest, user_id: UUID):
        products = db.query(Product).limit(2).all()

        product_context = "\n".join([
            f"- {p.name} | {p.price:,} VND | stock: {p.stock}"
            for p in products
        ])

        prompt = f"""
        Bạn là trợ lý bán hàng.
        Trả lời ngắn gọn tiếng Việt.

        Sản phẩm:
        {product_context}

        User: {req.message}
        """

        # 👉 AI response
        answer = chat_with_ai(prompt)
        start = time.time()
        answer = chat_with_ai(prompt)
        print("AI TIME:", time.time() - start)
        # 🔥 FIX NEWLINE (QUAN TRỌNG)
        answer = re.sub(r"\\n", "\n", answer)  # convert literal \n -> real newline
        answer = re.sub(r"\n{3,}", "\n\n", answer)  # normalize spacing

        # 👉 save chat
        if user_id is not None:
            db.add_all([
                AIChatHistory(
                    user_id=user_id,
                    role="user",
                    content=req.message
                ),
                AIChatHistory(
                    user_id=user_id,
                    role="assistant",
                    content=answer
                )
            ])
            db.commit()

        # 👉 return clean
        return {
            "message": req.message,
            "answer": answer
        }
