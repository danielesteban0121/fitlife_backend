from fastapi import Request
from fastapi.responses import JSONResponse

from src.domain.exceptions.base import DomainException


async def domain_exception_handler(
    request: Request,
    exc: DomainException,
):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )
