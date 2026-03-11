from uuid import UUID
from src.domain.repositories.nutrition_repository import NutritionRepository
from src.application.dtos.nutrition_dtos import NutritionPlanResponseDTO, DailyMealDTO

class GetActiveNutritionPlan:
    def __init__(self, nutrition_repository: NutritionRepository):
        self.nutrition_repository = nutrition_repository

    async def execute(self, user_id: UUID) -> NutritionPlanResponseDTO:
        plan = await self.nutrition_repository.get_active_plan_by_user(user_id)
        if not plan:
            return None # O lanzar DomainException("No active plan") dependiendo del diseño

        meals_dto = [
            DailyMealDTO(
                meal_type=m.meal_type,
                description=m.description,
                calories=m.calories,
                macros=m.macros
            )
            for m in plan.meals
        ]

        return NutritionPlanResponseDTO(
            plan_id=plan.id,
            user_id=plan.user_id,
            instructor_id=plan.instructor_id,
            target_calories=plan.target_calories,
            macro_distribution=plan.macro_distribution,
            start_date=plan.start_date,
            end_date=plan.end_date,
            meals=meals_dto,
            is_active=plan.is_active
        )
