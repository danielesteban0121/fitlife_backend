from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.assessment import Assessment
from src.domain.repositories.assessment_repository import (
    AssessmentRepository,
)
from src.infrastructure.database.models.assessment_model import (
    AssessmentModel,
)


class SQLAlchemyAssessmentRepository(AssessmentRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, assessment: Assessment):

        answers = [
            {
                "question_id": a.question_id,
                "answer": a.answer,
            }
            for a in assessment.answers
        ]

        model = AssessmentModel(
            user_id=assessment.user_id,
            fitness_score=assessment.fitness_score,
            answers=answers,
        )

        self.session.add(model)

        await self.session.commit()

        await self.session.refresh(model)

        return model
