from typing import List, Optional

from src.domain.entities.assessment_question import AssessmentQuestion, QuestionCategory
from src.domain.repositories.assessment_repository import AssessmentRepository


class GetAssessmentQuestions:
    """Caso de uso para obtener las preguntas habilitadas para el cuestionario inicial."""

    def __init__(self, repository: AssessmentRepository):
        self.repository = repository

    async def execute(self, category: Optional[QuestionCategory] = None) -> List[AssessmentQuestion]:
        return await self.repository.find_questions(category)
