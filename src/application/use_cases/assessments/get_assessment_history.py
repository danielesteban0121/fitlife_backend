from datetime import datetime
from src.application.dtos.assessment_dtos import AssessmentResponse
from src.domain.repositories.assessment_repository import AssessmentRepository


class GetAssessmentHistory:
    def __init__(self, repository: AssessmentRepository):
        self.repository = repository

    async def execute(self, user_id: str) -> list[AssessmentResponse]:
        assessments = await self.repository.find_history_by_user_id(user_id)

        return [
            AssessmentResponse(
                id=a.id,
                user_id=a.user_id,
                goal=a.goal,
                activity_level=a.activity_level,
                experience_level=a.experience_level,
                height_cm=a.height_cm,
                weight_kg=a.weight_kg,
                age=a.age,
                fitness_score=a.fitness_score,
                created_at=a.created_at or datetime.utcnow(),
            )
            for a in assessments
        ]
