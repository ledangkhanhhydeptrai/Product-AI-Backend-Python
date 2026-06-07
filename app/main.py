import uvicorn

from fastapi import FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router
from app.api.auth import router as auth_router
from app.api.product import router as product_router
from app.api.brand import router as brand_router
from app.api.category import router as category_router
from app.api.cart import router as cart_router
from app.api.order import router as order_router
from app.api.payment import router as payment_router
from app.api.review import router as review_router
from app.core import cloudinary_config

from app.exception.GlobalExceptionHandler import (
    custom_http_exception_handler
)

from app.core.database import Base, engine

app = FastAPI(
    title="Product AI API",
    description="Backend API for Product AI",
    version="1.0.0",
    docs_url=None,
    redoc_url=None
)


@app.get("/", include_in_schema=False)
async def custom_swagger():
    if app.openapi_url is None:
        raise RuntimeError("OpenAPI URL is not configured")

    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="Product AI"
    )


app.add_exception_handler(
    HTTPException,
    custom_http_exception_handler
)

app.include_router(auth_router)
app.include_router(category_router)

app.include_router(chat_router)

app.include_router(product_router)

app.include_router(brand_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(payment_router)
app.include_router(review_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    uvicorn.run(
        "app.main:app",
        host="localhost",
        port=8080,
        reload=True
    )
