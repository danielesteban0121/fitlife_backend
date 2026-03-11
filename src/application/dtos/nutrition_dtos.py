from datetime import date, datetime
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel

from src.domain.entities.nutrition import MealType


class DailyMeal(BaseModel):
    meal_type: MealType
    description: str
    calories: int
    macros: Dict[str, int]


class CreateNutritionPlanRequest(BaseModel):
    user_id: UUID
    instructor_id: UUID
    target_calories: int
    macro_distribution: Dict[str, float]
    start_date: date
    end_date: Optional[date] = None
    meals: List[DailyMeal]


class CreateNutritionPlanResponse(BaseModel):
    plan_id: UUID
    created_at: datetime
    message: str


class NutritionPlanResponse(BaseModel):
    id: str
    name: str
    description: str
    instructor_id: str
    is_active: bool
    created_at: datetime
    target_calories: Optional[int] = None
    macro_distribution: Optional[Dict[str, float]] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    meals: Optional[List[DailyMeal]] = None
