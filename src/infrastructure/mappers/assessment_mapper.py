from datetime import datetime
from uuid import UUID

from src.domain.entities.assessment import Assessment
from src.infrastructure.database.models.assessment_model import AssessmentModel


class AssessmentMapper:
    """Mapper para convertir entre la entidad Assessment y el modelo de BD."""

    @staticmethod
    def to_domain(model: AssessmentModel) -> Assessment:
        return Assessment(
            id=model.id,
            user_id=model.user_id,
            goal=model.goal,
            activity_level=model.activity_level,
            experience_level=model.experience_level,
            height_cm=model.height_cm,
            weight_kg=model.weight_kg,
            age=model.age,
            fitness_score=model.fitness_score,
            created_at=model.created_at,
        )

    @staticmethod
    def to_model(entity: Assessment) -> AssessmentModel:
        return AssessmentModel(
            id=entity.id,
            user_id=entity.user_id,
            goal=entity.goal,
            activity_level=entity.activity_level,
            experience_level=entity.experience_level,
            height_cm=entity.height_cm,
            weight_kg=entity.weight_kg,
            age=entity.age,
            fitness_score=entity.fitness_score,
            created_at=entity.created_at or datetime.utcnow(),
        )
