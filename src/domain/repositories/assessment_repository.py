from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities.assessment import Assessment
from src.domain.entities.assessment_question import AssessmentQuestion, QuestionCategory


class AssessmentRepository(ABC):

    @abstractmethod
    async def save(self, assessment: Assessment) -> Assessment:
        pass

    @abstractmethod
    async def find_by_user_id(self, user_id: str) -> Optional[Assessment]:
        pass

    @abstractmethod
    async def find_history_by_user_id(self, user_id: str) -> list[Assessment]:
        """Recupera el historial de evaluaciones de un usuario."""

    @abstractmethod
    async def delete_by_user_id(self, user_id: str) -> None:
        pass

    @abstractmethod
    async def find_questions(
        self, category: Optional[QuestionCategory] = None
    ) -> List[AssessmentQuestion]:
        """Recupera las preguntas de evaluación configuradas."""

    @abstractmethod
    async def save_question(self, question: AssessmentQuestion) -> AssessmentQuestion:
        """Guarda o actualiza una pregunta de evaluación."""

