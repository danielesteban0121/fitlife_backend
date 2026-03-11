
from src.application.dtos.training_dtos import AssignRoutineRequest
from src.application.services.notification_service import NotificationService
from src.domain.repositories.training_repository import TrainingRepository


class AssignRoutine:
    def __init__(self, repository: TrainingRepository, notification_service: NotificationService):
        self.repository = repository
        self.notification_service = notification_service

    async def execute(self, request: AssignRoutineRequest) -> bool:
        success = await self.repository.assign_routine(request.user_id, request.routine_id)

        if success:
            await self.notification_service.send_assignment_notification(
                user_id=request.user_id,
                assignment_type="Rutina de Entrenamiento",
                details={"routine_id": str(request.routine_id)},
            )

        return success
