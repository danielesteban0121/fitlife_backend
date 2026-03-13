from uuid import UUID

from src.domain.entities.assessment_question import AssessmentQuestion
from src.infrastructure.database.models.assessment_question_model import AssessmentQuestionModel


class AssessmentQuestionMapper:
    """Mapper para convertir entre la entidad de dominio y el modelo de BD."""

    @staticmethod
    def to_domain(model: AssessmentQuestionModel) -> AssessmentQuestion:
        return AssessmentQuestion(
            id=UUID(model.id),
            question_type=model.question_type,
            category=model.category,
            label=model.label,
            weight=model.weight,
            display_order=model.display_order,
            constraints=model.constraints,
            options=model.options,
            is_active=model.is_active,
        )

    @staticmethod
    def to_model(entity: AssessmentQuestion) -> AssessmentQuestionModel:
        return AssessmentQuestionModel(
            id=str(entity.id),
            question_type=entity.question_type,
            category=entity.category,
            label=entity.label,
            weight=entity.weight,
            display_order=entity.display_order,
            constraints=entity.constraints,
            options=entity.options,
            is_active=entity.is_active,
        )
