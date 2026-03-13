"""
Rutas API para el seguimiento del progreso físico (Physical Records).

Endpoints:
- POST /api/physical-records         → Registrar nuevas medidas
- GET  /api/physical-records/history  → Ver historial de progreso
"""
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from src.adapters.api.dependencies import get_current_user
from src.adapters.api.dependencies_phase_f import (
    get_create_physical_record,
    get_get_physical_history,
)
from src.application.dtos.physical_record_dtos import (
    CreatePhysicalRecordRequest,
    PhysicalRecordResponse,
)

router = APIRouter(prefix="/api/physical-records", tags=["Physical Progress"])


@router.post("", response_model=PhysicalRecordResponse, status_code=201)
async def create_record(
    request: CreatePhysicalRecordRequest,
    current_user: dict = Depends(get_current_user),
    use_case=Depends(get_create_physical_record),
):
    """Registra una nueva medición física para el usuario autenticado."""
    user_id = UUID(current_user["user_id"])
    return await use_case.execute(user_id, request)


@router.get("/history", response_model=List[PhysicalRecordResponse])
async def get_history(
    current_user: dict = Depends(get_current_user),
    use_case=Depends(get_get_physical_history),
):
    """Retorna todas las mediciones previas del usuario autenticado."""
    user_id = UUID(current_user["user_id"])
    return await use_case.execute(user_id)
