from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import date, datetime
from uuid import UUID
from src.domain.entities.nutrition import MealType

class DailyMealDTO(BaseModel):
    meal_type: MealType
    description: str
    calories: int
    macros: Dict[str, int]

class CreateNutritionPlanRequestDTO(BaseModel):
    user_id: UUID
    instructor_id: UUID
    target_calories: int
    macro_distribution: Dict[str, float]
    start_date: date
    end_date: Optional[date] = None
    meals: List[DailyMealDTO]

class CreateNutritionPlanResponseDTO(BaseModel):
    plan_id: UUID
    created_at: datetime
    message: str

class NutritionPlanResponseDTO(BaseModel):
    plan_id: UUID
    user_id: UUID
    instructor_id: UUID
    target_calories: int
    macro_distribution: Dict[str, float]
    start_date: date
    end_date: Optional[date]
    meals: List[DailyMealDTO]
    is_active: bool
