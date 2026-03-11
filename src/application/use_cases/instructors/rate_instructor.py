from src.domain.repositories.instructor_repository import InstructorRepository
from src.domain.exceptions.base import DomainException
from src.application.dtos.instructor_dtos import RateInstructorRequestDTO, RateInstructorResponseDTO

class RateInstructor:
    def __init__(self, instructor_repository: InstructorRepository):
        self.instructor_repository = instructor_repository

    async def execute(self, request: RateInstructorRequestDTO) -> RateInstructorResponseDTO:
        instructor = await self.instructor_repository.find_by_id(request.instructor_id)
        if not instructor:
            raise DomainException(f"Instructor {request.instructor_id} no encontrado")

        # Fake current rate count (we'd need a rating table to count actual)
        # for simplicity assuming a fixed amount to just perform the calculation from Domain
        TOTAL_FAKE_RATINGS = 5 
        new_avg = instructor.calculate_new_rating(request.rating, TOTAL_FAKE_RATINGS)
        
        await self.instructor_repository.save(instructor)

        return RateInstructorResponseDTO(
            instructor_id=instructor.id,
            new_average_rating=new_avg
        )
