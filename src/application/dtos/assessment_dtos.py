from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from src.domain.entities.assessment import ActivityLevel, ExperienceLevel, FitnessGoal


class SubmitAssessmentRequest(BaseModel):
    goal: FitnessGoal
    activity_level: ActivityLevel
    experience_level: ExperienceLevel
    height_cm: float = Field(gt=0, description="Height in centimeters")
    weight_kg: float = Field(gt=0, description="Weight in kilograms")
    age: int = Field(gt=0, description="Age in years")

    model_config = ConfigDict(use_enum_values=True)


class AssessmentResponse(BaseModel):
    id: str
    user_id: str
    goal: FitnessGoal
    activity_level: ActivityLevel
    experience_level: ExperienceLevel
    height_cm: float
    weight_kg: float
    age: int
    fitness_score: Optional[float]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
