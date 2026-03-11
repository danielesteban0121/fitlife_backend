from src.domain.entities.instructor import InstructorAssignment
from src.domain.repositories.instructor_repository import InstructorRepository
from src.domain.repositories.user_repository import UserRepository
from src.domain.exceptions.base import DomainException
from src.application.dtos.instructor_dtos import (
    AssignInstructorRequestDTO,
    AssignInstructorResponseDTO,
)
import uuid


class AssignInstructor:
    def __init__(
        self, instructor_repository: InstructorRepository, user_repository: UserRepository
    ):
        self.instructor_repository = instructor_repository
        self.user_repository = user_repository

    async def execute(self, request: AssignInstructorRequestDTO) -> AssignInstructorResponseDTO:
        user = await self.user_repository.find_by_id(request.user_id)
        if not user:
            raise DomainException(f"User {request.user_id} no encontrado")

        instructor = await self.instructor_repository.find_by_id(request.instructor_id)
        if not instructor:
            raise DomainException(f"Instructor {request.instructor_id} no encontrado")

        # Check if already has an active assignment
        active_assignment = await self.instructor_repository.get_active_assignment_for_user(
            request.user_id
        )
        if active_assignment:
            # Desactivar la asignación anterior
            active_assignment.deactivate()
            await self.instructor_repository.save_assignment(active_assignment)

            # Restar contador de alumnos activos
            prev_instructor = await self.instructor_repository.find_by_id(
                active_assignment.instructor_id
            )
            if prev_instructor and prev_instructor.active_users_count > 0:
                prev_instructor.active_users_count -= 1
                await self.instructor_repository.save(prev_instructor)

        # Crear nueva asignacion
        new_assignment = InstructorAssignment(
            id=uuid.uuid4(), user_id=request.user_id, instructor_id=request.instructor_id
        )

        saved_assignment = await self.instructor_repository.save_assignment(new_assignment)

        # Sumar contador
        instructor.active_users_count += 1
        await self.instructor_repository.save(instructor)

        return AssignInstructorResponseDTO(
            assignment_id=saved_assignment.id,
            user_id=saved_assignment.user_id,
            instructor_id=saved_assignment.instructor_id,
            is_active=saved_assignment.is_active,
            assigned_at=saved_assignment.assigned_at,
        )
