from uuid import uuid4

from src.application.dtos.nutrition_dtos import CreateNutritionPlanRequest, NutritionPlanResponse
from src.domain.entities.nutrition import NutritionPlan
from src.domain.repositories.nutrition_repository import NutritionRepository


class CreateNutritionPlan:
    def __init__(self, repository: NutritionRepository):
        self.repository = repository

    async def execute(self, request: CreateNutritionPlanRequest) -> NutritionPlanResponse:
        plan = NutritionPlan(
            id=uuid4(),
            user_id=request.user_id,
            instructor_id=request.instructor_id,
            target_calories=request.target_calories,
            macro_distribution=request.macro_distribution,
            start_date=request.start_date,
            end_date=request.end_date,
            meals=[],
        )
        saved_plan = await self.repository.save_plan(plan)

        return NutritionPlanResponse(
            id=str(saved_plan.id),
            instructor_id=str(saved_plan.instructor_id),
            is_active=saved_plan.is_active,
            created_at=saved_plan.created_at,
            target_calories=saved_plan.target_calories,
            macro_distribution=saved_plan.macro_distribution,
            start_date=saved_plan.start_date,
            end_date=saved_plan.end_date,
        )
