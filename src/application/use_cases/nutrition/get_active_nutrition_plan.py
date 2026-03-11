from datetime import datetime
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
            name=plan.name,
            description=plan.description,
            instructor_id=str(plan.instructor_id),
            is_active=True,
            created_at=datetime.utcnow()  # In a real scenario, this would come from the plan itself
        )
