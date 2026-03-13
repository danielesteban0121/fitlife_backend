"""Rutas de autenticación: registro, login, refresh, cambio y reset de contraseña."""
from fastapi import APIRouter, Depends, Request

from src.adapters.api.dependencies import (
    get_current_user,
    get_login_user,
    get_refresh_token,
    get_register_user,
)
from src.adapters.api.dependencies_phase_f import (
    get_change_password,
    get_reset_password,
    get_reset_password_request,
)
from src.adapters.api.schemas.auth_schemas import (
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
)
from src.application.dtos.auth_dtos import (
    ChangePasswordRequest,
    MessageResponse,
    RegisterUserRequest,
    ResetPasswordDTO,
    ResetPasswordRequestDTO,
)
from src.config.limiter import limiter

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register", response_model=TokenResponse)
@limiter.limit("5/minute")
async def register(
    request: Request,
    data: RegisterRequest,
    use_case=Depends(get_register_user),
):
    """Registra un nuevo usuario y retorna tokens JWT."""
    dto = RegisterUserRequest(email=data.email, password=data.password)
    return await use_case.execute(dto)


@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
async def login(
    request: Request,
    data: LoginRequest,
    use_case=Depends(get_login_user),
):
    """Autentica un usuario y retorna tokens JWT."""
    return await use_case.execute(email=data.email, password=data.password)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    data: RefreshRequest,
    use_case=Depends(get_refresh_token),
):
    """Renueva el access token usando un refresh token válido."""
    return await use_case.execute(data.token)


@router.post("/change-password", response_model=MessageResponse)
async def change_password(
    data: ChangePasswordRequest,
    current_user: dict = Depends(get_current_user),
    use_case=Depends(get_change_password),
):
    """Cambia la contraseña del usuario autenticado."""
    from uuid import UUID
    user_id = UUID(current_user["user_id"])
    return await use_case.execute(user_id, data)


@router.post("/forgot-password", response_model=MessageResponse)
@limiter.limit("3/minute")
async def forgot_password(
    request: Request,
    data: ResetPasswordRequestDTO,
    use_case=Depends(get_reset_password_request),
):
    """Envía un email con el enlace para restablecer contraseña."""
    return await use_case.execute(data)


@router.post("/reset-password", response_model=MessageResponse)
async def reset_password(
    data: ResetPasswordDTO,
    use_case=Depends(get_reset_password),
):
    """Establece una nueva contraseña usando el token recibido por email."""
    return await use_case.execute(data)
