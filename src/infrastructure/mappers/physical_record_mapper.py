from uuid import UUID

from src.domain.entities.physical_record import PhysicalRecord
from src.infrastructure.database.models.physical_record_model import PhysicalRecordModel


class PhysicalRecordMapper:
    """Mapper para convertir entre la entidad de dominio y el modelo de BD."""

    @staticmethod
    def to_domain(model: PhysicalRecordModel) -> PhysicalRecord:
        return PhysicalRecord(
            id=UUID(model.id),
            user_id=UUID(model.user_id),
            weight_kg=model.weight_kg,
            height_cm=model.height_cm,
            body_fat_percentage=model.body_fat_percentage,
            muscle_mass_kg=model.muscle_mass_kg,
            waist_cm=model.waist_cm,
            chest_cm=model.chest_cm,
            hips_cm=model.hips_cm,
            notes=model.notes,
            recorded_at=model.recorded_at,
        )

    @staticmethod
    def to_model(entity: PhysicalRecord) -> PhysicalRecordModel:
        return PhysicalRecordModel(
            id=str(entity.id),
            user_id=str(entity.user_id),
            weight_kg=entity.weight_kg,
            height_cm=entity.height_cm,
            body_fat_percentage=entity.body_fat_percentage,
            muscle_mass_kg=entity.muscle_mass_kg,
            waist_cm=entity.waist_cm,
            chest_cm=entity.chest_cm,
            hips_cm=entity.hips_cm,
            notes=entity.notes,
            recorded_at=entity.recorded_at,
        )
