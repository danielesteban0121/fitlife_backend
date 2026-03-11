from src.domain.repositories.instructor_repository import InstructorRepository
from src.application.dtos.instructor_dtos import ListInstructorsResponseDTO, InstructorResponseDTO


class ListInstructors:
    def __init__(self, instructor_repository: InstructorRepository):
        self.instructor_repository = instructor_repository

    async def execute(self, skip: int = 0, limit: int = 100) -> ListInstructorsResponseDTO:
        instructors = await self.instructor_repository.get_all(skip=skip, limit=limit)

        dto_list = [
            InstructorResponseDTO(
                id=inst.id,
                user_id=inst.user_id,
                certifications=inst.certifications,
                specializations=inst.specializations,
                average_rating=inst.average_rating,
                active_users_count=inst.active_users_count,
            )
            for inst in instructors
        ]

        return ListInstructorsResponseDTO(instructors=dto_list, total=len(dto_list))
