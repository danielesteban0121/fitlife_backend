from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import UUID


class RoutineExerciseDTO(BaseModel):
    exercise_id: UUID
    target_sets: int
    target_reps: int
    rest_seconds: int
    notes: Optional[str] = None


class CreateRoutineRequestDTO(BaseModel):
    user_id: UUID
    instructor_id: UUID
    title: str
    description: str
    exercises: List[RoutineExerciseDTO]


class CreateRoutineResponseDTO(BaseModel):
    routine_id: UUID
    title: str
    created_at: datetime


class AssignRoutineRequestDTO(BaseModel):
    routine_id: UUID
    user_id: UUID


class AssignRoutineResponseDTO(BaseModel):
    success: bool
    message: str


class CompleteWorkoutRequestDTO(BaseModel):
    routine_id: UUID
    user_id: UUID
    notes: Optional[str] = None
    duration_minutes: Optional[int] = None


class CompleteWorkoutResponseDTO(BaseModel):
    log_id: UUID
    routine_id: UUID
    completed_at: datetime
