# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/

from fastapi import FastAPI
from sqlalchemy import text

from app.api.chat import router as chat_router
from app.core.database import engine

app = FastAPI(
    title="AI Ecommerce Backend",
    docs_url="/",
    redoc_url="/redoc",
)

app.include_router(chat_router, prefix="/api")


@app.get("/test")
def root():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

    return {
        "message": "Database connected",
        "result": result.scalar()
    }
