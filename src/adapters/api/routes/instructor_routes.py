from fastapi import APIRouter, Depends
from src.adapters.api.dependencies import get_current_user
from src.adapters.api.dependencies_phase_f import (
    get_list_instructors,
    get_assign_instructor,
    get_rate_instructor,
)
from src.application.dtos.instructor_dtos import (
    ListInstructorsResponseDTO,
    AssignInstructorRequestDTO,
    AssignInstructorResponseDTO,
    RateInstructorRequestDTO,
    RateInstructorResponseDTO,
)

router = APIRouter(prefix="/api/instructors", tags=["Instructors"])


@router.get("/", response_model=ListInstructorsResponseDTO)
async def list_instructors(
    skip: int = 0,
    limit: int = 100,
    use_case=Depends(get_list_instructors),
    current_user: dict = Depends(get_current_user),
):
    return await use_case.execute(skip, limit)


@router.post("/assign", response_model=AssignInstructorResponseDTO)
async def assign_instructor(
    request: AssignInstructorRequestDTO,
    use_case=Depends(get_assign_instructor),
    current_user: dict = Depends(get_current_user),
):
    return await use_case.execute(request)


@router.post("/rate", response_model=RateInstructorResponseDTO)
async def rate_instructor(
    request: RateInstructorRequestDTO,
    use_case=Depends(get_rate_instructor),
    current_user: dict = Depends(get_current_user),
):
    return await use_case.execute(request)
