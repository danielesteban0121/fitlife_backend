from src.domain.entities.assessment import Assessment
from src.domain.entities.assessment import AssessmentAnswer
from src.domain.repositories.assessment_repository import (
    AssessmentRepository,
)
from src.domain.services.assessment_calculator import (
    AssessmentCalculator,
)
from src.application.dtos.assessment_dtos import SubmitAssessmentDTO


class SubmitAssessmentUseCase:

    def __init__(self, repository: AssessmentRepository):
        self.repository = repository

    async def execute(self, dto: SubmitAssessmentDTO):

        answers = [
            AssessmentAnswer(
                question_id=a.question_id,
                answer=a.answer,
            )
            for a in dto.answers
        ]

        fitness_score = AssessmentCalculator.calculate(answers)

        assessment = Assessment(
            user_id=dto.user_id,
            answers=answers,
            fitness_score=fitness_score,
        )

        return await self.repository.save(assessment)
