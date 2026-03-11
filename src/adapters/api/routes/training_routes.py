from fastapi import APIRouter, Depends
from src.adapters.api.dependencies import get_current_user
from src.adapters.api.dependencies_phase_f import (
    get_create_routine,
    get_assign_routine,
    get_complete_workout,
)
from src.application.dtos.training_dtos import (
    CreateRoutineRequest,
    CreateRoutineResponse,
    AssignRoutineRequest,
    AssignRoutineResponse,
    CompleteWorkoutRequest,
    CompleteWorkoutResponse,
)

router = APIRouter(prefix="/api/training", tags=["Training"])


@router.post("/routines", response_model=CreateRoutineResponse)
async def create_routine(
    request: CreateRoutineRequest,
    use_case=Depends(get_create_routine),
    current_user: dict = Depends(get_current_user),
):
    # Depending on RBAC, instructor only
    return await use_case.execute(request)


@router.post("/routines/assign", response_model=AssignRoutineResponse)
async def assign_routine(
    request: AssignRoutineRequest,
    use_case=Depends(get_assign_routine),
    current_user: dict = Depends(get_current_user),
):
    return await use_case.execute(request)


@router.post("/workouts/complete", response_model=CompleteWorkoutResponse)
async def complete_workout(
    request: CompleteWorkoutRequest,
    use_case=Depends(get_complete_workout),
    current_user: dict = Depends(get_current_user),
):
    return await use_case.execute(request)
