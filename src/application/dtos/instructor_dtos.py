from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from uuid import UUID


class InstructorResponse(BaseModel):
    id: UUID
    user_id: UUID
    certifications: List[str]
    specializations: List[str]
    average_rating: float
    active_users_count: int


class ListInstructorsResponse(BaseModel):
    instructors: List[InstructorResponse]
    total: int


class AssignInstructorRequest(BaseModel):
    user_id: UUID
    instructor_id: UUID


class AssignInstructorResponse(BaseModel):
    assignment_id: UUID
    user_id: UUID
    instructor_id: UUID
    is_active: bool
    assigned_at: datetime


class RateInstructorRequest(BaseModel):
    instructor_id: UUID
    rating: float = Field(..., ge=1.0, le=5.0)


class RateInstructorResponse(BaseModel):
    instructor_id: UUID
    new_average_rating: float
