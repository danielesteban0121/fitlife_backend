from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict
from uuid import UUID


@dataclass
class Instructor:
    """Entidad de dominio para Instructor."""

    id: UUID
    user_id: UUID
    certifications: List[str]
    specializations: List[str]
    average_rating: float = 0.0
    active_users_count: int = 0

    def calculate_new_rating(self, new_rating: float, total_ratings_count: int) -> float:
        """Actualiza el rating promedio basado en una nueva calificación."""
        current_total = self.average_rating * (total_ratings_count - 1)
        self.average_rating = round((current_total + new_rating) / total_ratings_count, 2)
        return self.average_rating


@dataclass
class InstructorAssignment:
    """Entidad para la asignación de un instructor a un usuario."""

    id: UUID
    user_id: UUID
    instructor_id: UUID
    is_active: bool = True
    assigned_at: datetime = field(default_factory=datetime.utcnow)
    ended_at: Optional[datetime] = None

    def deactivate(self, ended_at: Optional[datetime] = None):
        self.is_active = False
        self.ended_at = ended_at or datetime.utcnow()
