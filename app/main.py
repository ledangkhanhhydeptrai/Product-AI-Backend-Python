import uvicorn
from fastapi import FastAPI
from sqlalchemy import text

from app.api.chat import router as chat_router
from app.core.database import engine, Base

from app.models.user import User
from app.models.category import Category
from app.models.product import Product
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.review import Review
from app.models.ai_chat_histories import AIChatHistory


app = FastAPI(
    title="AI Ecommerce Backend",
    docs_url="/",
    redoc_url="/redoc",
)

app.include_router(chat_router, prefix="/api")

Base.metadata.create_all(bind=engine)


@app.get("/test")
def root():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

    return {
        "message": "Database connected",
        "result": result.scalar()
    }


if __name__ == '__main__':
    uvicorn.run(
        "app.main:app",
        host="localhost",
        port=8080,
        reload=True
    )