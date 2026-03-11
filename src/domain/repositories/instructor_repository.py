from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from ..entities.instructor import Instructor, InstructorAssignment


class InstructorRepository(ABC):
    """Puerto de salida para persistencia de instructores y asignaciones."""

    @abstractmethod
    async def save(self, instructor: Instructor) -> Instructor:
        pass

    @abstractmethod
    async def find_by_id(self, instructor_id: UUID) -> Optional[Instructor]:
        pass

    @abstractmethod
    async def find_by_user_id(self, user_id: UUID) -> Optional[Instructor]:
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Instructor]:
        pass

    @abstractmethod
    async def save_assignment(self, assignment: InstructorAssignment) -> InstructorAssignment:
        pass

    @abstractmethod
    async def get_active_assignment_for_user(self, user_id: UUID) -> Optional[InstructorAssignment]:
        pass
