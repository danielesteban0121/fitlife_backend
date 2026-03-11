from uuid import UUID

from src.domain.entities.nutrition import NutritionPlan, DailyMeal
from src.infrastructure.database.models.nutrition_models import NutritionPlanModel, DailyMealModel

class NutritionMapper:
    @staticmethod
    def plan_to_domain(model: NutritionPlanModel) -> NutritionPlan:
        meals = [NutritionMapper.meal_to_domain(m) for m in model.meals] if model.meals else []
        return NutritionPlan(
            id=UUID(model.id),
            user_id=UUID(model.user_id),
            instructor_id=UUID(model.instructor_id),
            target_calories=model.target_calories,
            macro_distribution=model.macro_distribution,
            start_date=model.start_date,
            end_date=model.end_date,
            created_at=model.created_at,
            is_active=model.is_active,
            meals=meals
        )

    @staticmethod
    def plan_to_model(domain: NutritionPlan) -> NutritionPlanModel:
        return NutritionPlanModel(
            id=str(domain.id),
            user_id=str(domain.user_id),
            instructor_id=str(domain.instructor_id),
            target_calories=domain.target_calories,
            macro_distribution=domain.macro_distribution,
            start_date=domain.start_date,
            end_date=domain.end_date,
            created_at=domain.created_at,
            is_active=domain.is_active
        )
    
    @staticmethod
    def meal_to_domain(model: DailyMealModel) -> DailyMeal:
        return DailyMeal(
            id=UUID(model.id),
            meal_type=model.meal_type,
            description=model.description,
            calories=model.calories,
            macros=model.macros
        )
    
    @staticmethod
    def meal_to_model(domain: DailyMeal, plan_id: str) -> DailyMealModel:
        return DailyMealModel(
            id=str(domain.id),
            plan_id=plan_id,
            meal_type=domain.meal_type,
            description=domain.description,
            calories=domain.calories,
            macros=domain.macros
        )
