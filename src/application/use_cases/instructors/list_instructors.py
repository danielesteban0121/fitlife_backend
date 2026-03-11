from src.application.dtos.instructor_dtos import InstructorResponse, ListInstructorsResponse
from src.domain.repositories.instructor_repository import InstructorRepository


class ListInstructors:
    def __init__(self, instructor_repository: InstructorRepository):
        self.instructor_repository = instructor_repository

    async def execute(self, skip: int = 0, limit: int = 100) -> ListInstructorsResponse:
        instructors = await self.instructor_repository.get_all(skip=skip, limit=limit)

        dto_list = [
            InstructorResponse(
                id=inst.id,
                user_id=inst.user_id,
                certifications=inst.certifications,
                specializations=inst.specializations,
                average_rating=inst.average_rating,
                active_users_count=inst.active_users_count,
            )
            for inst in instructors
        ]

        return ListInstructorsResponse(instructors=dto_list, total=len(dto_list))
