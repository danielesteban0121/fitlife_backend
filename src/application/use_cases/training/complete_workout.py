import uuid
from src.domain.entities.training import WorkoutLog
from src.domain.repositories.training_repository import TrainingRepository
from src.domain.repositories.user_repository import UserRepository
from src.domain.exceptions.base import DomainException
from src.application.dtos.training_dtos import CompleteWorkoutRequestDTO, CompleteWorkoutResponseDTO

class CompleteWorkout:
    def __init__(
        self,
        training_repository: TrainingRepository,
        user_repository: UserRepository
    ):
        self.training_repository = training_repository
        self.user_repository = user_repository

    async def execute(self, request: CompleteWorkoutRequestDTO) -> CompleteWorkoutResponseDTO:
        user = await self.user_repository.find_by_id(request.user_id)
        if not user:
            raise DomainException(f"User {request.user_id} no encontrado")

        routine = await self.training_repository.find_routine_by_id(request.routine_id)
        if not routine:
            raise DomainException(f"Routine {request.routine_id} no encontrada")

        workout_log = WorkoutLog(
            id=uuid.uuid4(),
            routine_id=request.routine_id,
            user_id=request.user_id,
            notes=request.notes,
            duration_minutes=request.duration_minutes
        )

        saved_log = await self.training_repository.save_workout_log(workout_log)

        return CompleteWorkoutResponseDTO(
            log_id=saved_log.id,
            routine_id=saved_log.routine_id,
            completed_at=saved_log.completed_at
        )
