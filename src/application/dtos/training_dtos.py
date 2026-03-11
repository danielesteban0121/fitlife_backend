from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class RoutineExercise(BaseModel):
    exercise_id: UUID
    target_sets: int
    target_reps: int
    rest_seconds: int
    notes: Optional[str] = None


class CreateRoutineRequest(BaseModel):
    user_id: UUID
    instructor_id: UUID
    title: str
    description: str
    exercises: List[RoutineExercise]


class RoutineResponse(BaseModel):
    id: str
    name: str
    description: str
    instructor_id: str
    created_at: datetime


class CreateRoutineResponse(BaseModel):
    routine_id: UUID
    title: str
    created_at: datetime


class AssignRoutineRequest(BaseModel):
    routine_id: UUID
    user_id: UUID


class AssignRoutineResponse(BaseModel):
    success: bool
    message: str


class CompleteWorkoutRequest(BaseModel):
    routine_id: UUID
    user_id: UUID
    notes: Optional[str] = None
    duration_minutes: Optional[int] = None


class CompleteWorkoutResponse(BaseModel):
    log_id: UUID
    routine_id: UUID
    completed_at: datetime
