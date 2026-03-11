from datetime import datetime
from uuid import UUID, uuid4

from src.application.dtos.nutrition_dtos import CreateNutritionPlanRequest, NutritionPlanResponse
from src.domain.entities.nutrition import NutritionPlan
from src.domain.repositories.nutrition_repository import NutritionRepository


class CreateNutritionPlan:
    def __init__(self, repository: NutritionRepository):
        self.repository = repository

    async def execute(
        self, instructor_id: UUID, request: CreateNutritionPlanRequest
    ) -> NutritionPlanResponse:
        plan = NutritionPlan(
            id=uuid4(),
            name=request.name,
            description=request.description,
            instructor_id=instructor_id,
            meals=[],
        )
        saved_plan = await self.repository.save_plan(plan)

        return NutritionPlanResponse(
            id=str(saved_plan.id),
            name=saved_plan.name,
            description=saved_plan.description,
            instructor_id=str(saved_plan.instructor_id),
            is_active=True,
            created_at=datetime.utcnow(),
        )
