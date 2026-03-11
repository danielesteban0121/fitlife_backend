from fastapi import APIRouter, Depends
from uuid import UUID
from src.adapters.api.dependencies import get_current_user
from src.adapters.api.dependencies_phase_f import (
    get_create_nutrition_plan,
    get_get_active_nutrition_plan,
)
from src.application.dtos.nutrition_dtos import (
    CreateNutritionPlanRequestDTO,
    CreateNutritionPlanResponseDTO,
    NutritionPlanResponseDTO,
)

router = APIRouter(prefix="/api/nutrition", tags=["Nutrition"])


@router.post("/plans", response_model=CreateNutritionPlanResponseDTO)
async def create_nutrition_plan(
    request: CreateNutritionPlanRequestDTO,
    use_case=Depends(get_create_nutrition_plan),
    current_user: dict = Depends(get_current_user),
):
    return await use_case.execute(request)


@router.get("/plans/active/{user_id}", response_model=NutritionPlanResponseDTO)
async def get_active_nutrition_plan(
    user_id: UUID,
    use_case=Depends(get_get_active_nutrition_plan),
    current_user: dict = Depends(get_current_user),
):
    plan = await use_case.execute(user_id)
    if not plan:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="No active plan found")
    return plan
