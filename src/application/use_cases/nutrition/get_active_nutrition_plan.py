from uuid import UUID

from src.application.dtos.nutrition_dtos import NutritionPlanResponse
from src.domain.repositories.nutrition_repository import NutritionRepository


class GetActiveNutritionPlan:
    def __init__(self, repository: NutritionRepository):
        self.repository = repository

    async def execute(self, user_id: UUID) -> NutritionPlanResponse | None:
        plan = await self.repository.find_active_by_user_id(user_id)

        if not plan:
            return None

        return NutritionPlanResponse(
            id=str(plan.id),
            instructor_id=str(plan.instructor_id),
            is_active=plan.is_active,
            created_at=plan.created_at,
            target_calories=plan.target_calories,
            macro_distribution=plan.macro_distribution,
            start_date=plan.start_date,
            end_date=plan.end_date,
        )
