from fastapi import Request
from fastapi.responses import JSONResponse


async def custom_http_exception_handler(
        request: Request,
        exc: Exception
):
    status_code = getattr(exc, "status_code", 500)
    detail = getattr(exc, "detail", "Internal Server Error")

    return JSONResponse(
        status_code=status_code,
        content={
            "status": status_code,
            "message": detail,
            "data": None
        }
    )
