from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID

class InstructorResponseDTO(BaseModel):
    id: UUID
    user_id: UUID
    certifications: List[str]
    specializations: List[str]
    average_rating: float
    active_users_count: int

class ListInstructorsResponseDTO(BaseModel):
    instructors: List[InstructorResponseDTO]
    total: int

class AssignInstructorRequestDTO(BaseModel):
    user_id: UUID
    instructor_id: UUID

class AssignInstructorResponseDTO(BaseModel):
    assignment_id: UUID
    user_id: UUID
    instructor_id: UUID
    is_active: bool
    assigned_at: datetime

class RateInstructorRequestDTO(BaseModel):
    instructor_id: UUID
    rating: float = Field(..., ge=1.0, le=5.0)

class RateInstructorResponseDTO(BaseModel):
    instructor_id: UUID
    new_average_rating: float
