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
            .order_by(asc(AIChatHistory.id))
            .all()
        )

    @staticmethod
    def chat(db: Session, req: ChatRequest, user_id: UUID):

        try:
            # 1. Get products from DB
            products = (
                db.query(Product)
                .limit(5)
                .all()
            )

            product_context = "\n".join([
                f"- {p.name} | {p.price:,} VND | stock: {p.stock}"
                for p in products
            ])

            # 2. Build prompt for AI
            prompt = f"""
            Bạn là hệ thống API.

            🚨 QUY TẮC TUYỆT ĐỐI:
            - CHỈ được trả về JSON
            - KHÔNG được giải thích
            - KHÔNG markdown
            - KHÔNG text bên ngoài JSON
            - KHÔNG \n, KHÔNG **, KHÔNG dấu câu ngoài JSON

            📦 DATA:
            {product_context}

            👤 USER:
            {req.message}

            📤 OUTPUT FORMAT:
            Trả về DUY NHẤT 1 JSON hợp lệ:

            {{
              "answer": string,
              "products": [
                {{
                  "name": string,
                  "price": number,
                  "reason": string
                }}
              ]
            }}
            """

            # 3. Call AI
            answer = chat_with_ai(prompt)

            # 4. Save chat history
            messages = [
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
            ]

            db.add_all(messages)
            db.commit()

            return {
                "message": req.message,
                "response": answer
            }

        except Exception as e:
            db.rollback()
            return {
                "message": req.message,
                "error": str(e)
            }
