from datetime import datetime
from uuid import UUID, uuid4

from src.application.dtos.training_dtos import CreateRoutineRequest, RoutineResponse
from src.domain.entities.training import Routine
from src.domain.repositories.training_repository import TrainingRepository


class CreateRoutine:
    def __init__(self, repository: TrainingRepository):
        self.repository = repository

    async def execute(self, instructor_id: UUID, request: CreateRoutineRequest) -> RoutineResponse:
        routine = Routine(
            id=uuid4(),
            name=request.name,
            description=request.description,
            instructor_id=instructor_id,
            exercises=[],  # Exercises would be added here in a more detailed flow
        )
        saved_routine = await self.repository.save_routine(routine)

        return RoutineResponse(
            id=str(saved_routine.id),
            name=saved_routine.name,
            description=saved_routine.description,
            instructor_id=str(saved_routine.instructor_id),
            created_at=datetime.utcnow(),
        )
