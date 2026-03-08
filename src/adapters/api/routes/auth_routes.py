from fastapi import APIRouter, Depends

from src.adapters.api.dependencies import (
    get_login_user,
    get_refresh_token,
    get_register_user,
)
from src.adapters.api.schemas.auth_schemas import (
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
)
from src.application.dtos.auth_dtos import RegisterUserRequest

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register", response_model=TokenResponse)
async def register(
    data: RegisterRequest,
    use_case=Depends(get_register_user),
):

    dto = RegisterUserRequest(
        email=data.email,
        password=data.password,
    )

    return await use_case.execute(dto)


@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    use_case=Depends(get_login_user),
):

    return await use_case.execute(
        email=data.email,
        password=data.password,
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    data: RefreshRequest,
    use_case=Depends(get_refresh_token),
):

    return await use_case.execute(data.token)
