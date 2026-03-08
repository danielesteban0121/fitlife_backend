from fastapi import Request
from fastapi.responses import JSONResponse

from src.domain.exceptions.base import DomainException
from src.domain.exceptions.user_exceptions import (
    InvalidCredentials,
    UserNotFoundException,
)


async def domain_exception_handler(
    request: Request,
    exc: DomainException,
):
    status_code = 400
    if isinstance(exc, (InvalidCredentials, UserNotFoundException)):
        status_code = 401

    return JSONResponse(
        status_code=status_code,
        content={"detail": str(exc)},
    )
