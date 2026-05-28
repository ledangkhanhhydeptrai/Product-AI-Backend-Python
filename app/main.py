import uvicorn

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.api.chat import router as chat_router
from app.api.auth import router as auth_router
from app.api.product import router as product_router
from app.core.database import engine, Base
from app.exception.GlobalExceptionHandler import (
    custom_http_exception_handler
)

app = FastAPI(
    title="AI Ecommerce Backend",
    docs_url="/",
    redoc_url="/redoc",
)

app.add_exception_handler(
    HTTPException,
    custom_http_exception_handler
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token"
)

app.include_router(auth_router)

app.include_router(
    chat_router,
    prefix="/api",
    dependencies=[Depends(oauth2_scheme)]
)
app.include_router(product_router)
Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    uvicorn.run(
        "app.main:app",
        host="localhost",
        port=8080,
        reload=True
    )
