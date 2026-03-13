from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID


class QuestionType(str, Enum):
    """Tipo de respuesta esperada para una pregunta de evaluación."""

    NUMERIC = "NUMERIC"
    SINGLE_CHOICE = "SINGLE_CHOICE"
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
    YES_NO = "YES_NO"


class QuestionCategory(str, Enum):
    """Categoría temática de la pregunta."""

    PHYSICAL = "PHYSICAL"
    FUNCTIONAL = "FUNCTIONAL"
    HABITS = "HABITS"
    ALERTS = "ALERTS"


@dataclass
class AssessmentQuestion:
    """
    Pregunta de evaluación física para el cuestionario.

    Permite definir evaluaciones dinámicas donde cada pregunta
    tiene su propio peso en el cálculo del fitness_score final.
    """

    id: UUID
    question_type: QuestionType
    category: QuestionCategory
    label: str
    weight: float = 1.0
    display_order: int = 0
    constraints: Dict[str, Any] = field(default_factory=dict)
    options: Optional[List[str]] = None
    is_active: bool = True

    def validate_answer(self, answer: Any) -> bool:
        """Valida que la respuesta sea coherente con el tipo de pregunta."""
        if self.question_type == QuestionType.YES_NO:
            return isinstance(answer, bool)
        if self.question_type == QuestionType.NUMERIC:
            if not isinstance(answer, (int, float)):
                return False
            min_val = self.constraints.get("min")
            max_val = self.constraints.get("max")
            if min_val is not None and answer < min_val:
                return False
            if max_val is not None and answer > max_val:
                return False
            return True
        if self.question_type == QuestionType.SINGLE_CHOICE:
            return self.options is not None and answer in self.options
        if self.question_type == QuestionType.MULTIPLE_CHOICE:
            return (
                self.options is not None
                and isinstance(answer, list)
                and all(a in self.options for a in answer)
            )
        return False
