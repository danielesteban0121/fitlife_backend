from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

class ExerciseCategory(str, Enum):
    CARDIO = "CARDIO"
    STRENGTH = "STRENGTH"
    FLEXIBILITY = "FLEXIBILITY"
    BALANCE = "BALANCE"
    OTHER = "OTHER"

@dataclass
class Exercise:
    """Entidad de dominio para un Ejercicio genérico."""
    id: UUID
    name: str
    description: str
    category: ExerciseCategory
    video_url: Optional[str] = None

@dataclass
class RoutineExercise:
    """Configuración de un ejercicio dentro de una rutina."""
    exercise_id: UUID
    target_sets: int
    target_reps: int
    rest_seconds: int
    notes: Optional[str] = None

@dataclass
class Routine:
    """Entidad de dominio para una Rutina de Entrenamiento."""
    id: UUID
    user_id: UUID
    instructor_id: UUID
    title: str
    description: str
    exercises: List[RoutineExercise] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    is_active: bool = True

@dataclass
class WorkoutLog:
    """Registro de la ejecución de una rutina."""
    id: UUID
    routine_id: UUID
    user_id: UUID
    completed_at: datetime = field(default_factory=datetime.utcnow)
    notes: Optional[str] = None
    duration_minutes: Optional[int] = None
