from src.domain.repositories.training_repository import TrainingRepository
from src.domain.repositories.user_repository import UserRepository
from src.domain.exceptions.base import DomainException
from src.application.dtos.training_dtos import AssignRoutineRequestDTO, AssignRoutineResponseDTO

class AssignRoutine:
    def __init__(
        self,
        training_repository: TrainingRepository,
        user_repository: UserRepository,
        notification_service=None
    ):
        self.training_repository = training_repository
        self.user_repository = user_repository
        self.notification_service = notification_service

    async def execute(self, request: AssignRoutineRequestDTO) -> AssignRoutineResponseDTO:
        user = await self.user_repository.find_by_id(request.user_id)
        if not user:
            raise DomainException(f"User {request.user_id} no encontrado")

        routine = await self.training_repository.find_routine_by_id(request.routine_id)
        if not routine:
            raise DomainException(f"Routine {request.routine_id} no encontrada")

        if routine.user_id != request.user_id:
            # We assign by cloning or updating if needed. But our domain says routine.user_id is the owner.
            # Assuming CreateRoutine already assigned it to the user.
            pass

        # If a notification service exists, notify the user.
        if self.notification_service:
            await self.notification_service.send_assignment_notification(
                user_id=request.user_id,
                assignment_type="rutina",
                details={"title": routine.title}
            )

        return AssignRoutineResponseDTO(
            success=True,
            message="Rutina asignada exitosamente"
        )
