import uuid
from src.domain.entities.training import Routine, RoutineExercise
from src.domain.repositories.training_repository import TrainingRepository
from src.domain.repositories.user_repository import UserRepository
from src.domain.repositories.instructor_repository import InstructorRepository
from src.domain.exceptions.base import DomainException
from src.application.dtos.training_dtos import CreateRoutineRequestDTO, CreateRoutineResponseDTO

class CreateRoutine:
    def __init__(
        self,
        training_repository: TrainingRepository,
        user_repository: UserRepository,
        instructor_repository: InstructorRepository
    ):
        self.training_repository = training_repository
        self.user_repository = user_repository
        self.instructor_repository = instructor_repository

    async def execute(self, request: CreateRoutineRequestDTO) -> CreateRoutineResponseDTO:
        user = await self.user_repository.find_by_id(request.user_id)
        if not user:
            raise DomainException(f"User {request.user_id} no encontrado")

        instructor = await self.instructor_repository.find_by_id(request.instructor_id)
        if not instructor:
            raise DomainException(f"Instructor {request.instructor_id} no encontrado")

        exercises_domain = [
            RoutineExercise(
                exercise_id=ex.exercise_id,
                target_sets=ex.target_sets,
                target_reps=ex.target_reps,
                rest_seconds=ex.rest_seconds,
                notes=ex.notes
            )
            for ex in request.exercises
        ]

        routine = Routine(
            id=uuid.uuid4(),
            user_id=request.user_id,
            instructor_id=request.instructor_id,
            title=request.title,
            description=request.description,
            exercises=exercises_domain
        )

        saved_routine = await self.training_repository.save_routine(routine)

        return CreateRoutineResponseDTO(
            routine_id=saved_routine.id,
            title=saved_routine.title,
            created_at=saved_routine.created_at
        )
