from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from ..entities.training import Routine, Exercise, WorkoutLog

class TrainingRepository(ABC):
    """Puerto de salida para persistencia de rutinas y ejercicios."""
    
    @abstractmethod
    async def save_routine(self, routine: Routine) -> Routine:
        pass
        
    @abstractmethod
    async def find_routine_by_id(self, routine_id: UUID) -> Optional[Routine]:
        pass

    @abstractmethod
    async def get_routines_by_user(self, user_id: UUID) -> List[Routine]:
        pass

    @abstractmethod
    async def get_all_exercises(self) -> List[Exercise]:
        pass
        
    @abstractmethod
    async def save_workout_log(self, log: WorkoutLog) -> WorkoutLog:
        pass

    @abstractmethod
    async def get_workout_history(self, user_id: UUID) -> List[WorkoutLog]:
        pass
