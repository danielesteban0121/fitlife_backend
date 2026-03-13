from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CreatePhysicalRecordRequest(BaseModel):
    weight_kg: float = Field(gt=0, description="Peso en kilogramos")
    height_cm: float = Field(gt=0, description="Altura en centímetros")
    body_fat_percentage: Optional[float] = Field(None, ge=0, le=100)
    muscle_mass_kg: Optional[float] = Field(None, ge=0)
    waist_cm: Optional[float] = Field(None, ge=0)
    chest_cm: Optional[float] = Field(None, ge=0)
    hips_cm: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = Field(None, max_length=500)


class PhysicalRecordResponse(BaseModel):
    id: UUID
    user_id: UUID
    weight_kg: float
    height_cm: float
    bmi: Optional[float]
    bmi_category: str
    body_fat_percentage: Optional[float]
    muscle_mass_kg: Optional[float]
    waist_cm: Optional[float]
    chest_cm: Optional[float]
    hips_cm: Optional[float]
    notes: Optional[str]
    recorded_at: datetime

    model_config = ConfigDict(from_attributes=True)
