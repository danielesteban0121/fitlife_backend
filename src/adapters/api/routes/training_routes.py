from fastapi import APIRouter, Depends
from src.adapters.api.dependencies import get_current_user
from src.adapters.api.dependencies_phase_f import (
    get_create_routine,
    get_assign_routine,
    get_complete_workout,
)
from src.application.dtos.training_dtos import (
    CreateRoutineRequestDTO,
    CreateRoutineResponseDTO,
    AssignRoutineRequestDTO,
    AssignRoutineResponseDTO,
    CompleteWorkoutRequestDTO,
    CompleteWorkoutResponseDTO,
)

router = APIRouter(prefix="/api/training", tags=["Training"])


@router.post("/routines", response_model=CreateRoutineResponseDTO)
async def create_routine(
    request: CreateRoutineRequestDTO,
    use_case=Depends(get_create_routine),
    current_user: dict = Depends(get_current_user),
):
    # Depending on RBAC, instructor only
    return await use_case.execute(request)


@router.post("/routines/assign", response_model=AssignRoutineResponseDTO)
async def assign_routine(
    request: AssignRoutineRequestDTO,
    use_case=Depends(get_assign_routine),
    current_user: dict = Depends(get_current_user),
):
    return await use_case.execute(request)


@router.post("/workouts/complete", response_model=CompleteWorkoutResponseDTO)
async def complete_workout(
    request: CompleteWorkoutRequestDTO,
    use_case=Depends(get_complete_workout),
    current_user: dict = Depends(get_current_user),
):
    return await use_case.execute(request)
