from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Dict, List, Optional
from uuid import UUID


class MealType(str, Enum):
    BREAKFAST = "BREAKFAST"
    LUNCH = "LUNCH"
    DINNER = "DINNER"
    SNACK = "SNACK"
    PRE_WORKOUT = "PRE_WORKOUT"
    POST_WORKOUT = "POST_WORKOUT"


@dataclass
class DailyMeal:
    """Entidad de comida recomendada dentro de un plan."""

    id: UUID
    meal_type: MealType
    description: str
    calories: int
    macros: Dict[str, int] = field(
        default_factory=dict
    )  # ej. {"protein": 30, "carbs": 40, "fat": 15}


@dataclass
class NutritionPlan:
    """Plan de nutrición asignado a un usuario."""

    id: UUID
    user_id: UUID
    instructor_id: UUID
    target_calories: int
    macro_distribution: Dict[str, float]  # ej. {"protein": 0.3, "carbs": 0.5, "fat": 0.2}
    start_date: date
    end_date: Optional[date] = None
    meals: List[DailyMeal] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    is_active: bool = True
