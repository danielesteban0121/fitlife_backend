from fastapi import APIRouter, Depends, status

from src.application.dtos.auth_dtos import (
    RegisterUserRequest,
    RegisterUserResponse,
)
from src.application.use_cases.auth.register_user import RegisterUser
from src.adapters.api.dependencies import get_register_user_use_case

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=RegisterUserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    request: RegisterUserRequest,
    use_case: RegisterUser = Depends(get_register_user_use_case),
):
    return await use_case.execute(request)
