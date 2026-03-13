"""
Rutas API para gestión del perfil de usuario.

Endpoints:
- GET  /api/users/me             → Perfil propio del usuario
- PATCH /api/users/me            → Actualizar perfil propio
- GET  /api/users/me/audit-log   → Historial de auditoría
"""
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from src.adapters.api.dependencies import get_current_user
from src.adapters.api.dependencies_phase_f import (
    get_get_profile_audit_log,
    get_get_user_profile,
    get_update_user_profile,
)
from src.application.dtos.user_dtos import (
    AuditLogResponse,
    UpdateUserProfileRequest,
    UserProfileResponse,
)

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("/me", response_model=UserProfileResponse)
async def get_my_profile(
    current_user: dict = Depends(get_current_user),
    use_case=Depends(get_get_user_profile),
):
    """Retorna el perfil del usuario autenticado."""
    user_id = UUID(current_user["user_id"])
    return await use_case.execute(user_id)


@router.patch("/me", response_model=UserProfileResponse)
async def update_my_profile(
    request: UpdateUserProfileRequest,
    current_user: dict = Depends(get_current_user),
    use_case=Depends(get_update_user_profile),
):
    """Actualiza el perfil del usuario autenticado."""
    user_id = UUID(current_user["user_id"])
    return await use_case.execute(user_id, request)


@router.get("/me/audit-log", response_model=List[AuditLogResponse])
async def get_my_audit_log(
    current_user: dict = Depends(get_current_user),
    use_case=Depends(get_get_profile_audit_log),
):
    """Retorna el historial de acciones del usuario autenticado."""
    user_id = UUID(current_user["user_id"])
    return await use_case.execute(user_id)
