from uuid import UUID, uuid4

from src.application.dtos.physical_record_dtos import CreatePhysicalRecordRequest, PhysicalRecordResponse
from src.domain.entities.physical_record import PhysicalRecord
from src.domain.repositories.physical_record_repository import PhysicalRecordRepository


class CreatePhysicalRecord:
    """Caso de uso para registrar nuevas mediciones corporales."""

    def __init__(self, repository: PhysicalRecordRepository):
        self.repository = repository

    async def execute(self, user_id: UUID, request: CreatePhysicalRecordRequest) -> PhysicalRecordResponse:
        record = PhysicalRecord(
            id=uuid4(),
            user_id=user_id,
            weight_kg=request.weight_kg,
            height_cm=request.height_cm,
            body_fat_percentage=request.body_fat_percentage,
            muscle_mass_kg=request.muscle_mass_kg,
            waist_cm=request.waist_cm,
            chest_cm=request.chest_cm,
            hips_cm=request.hips_cm,
            notes=request.notes
        )

        saved_record = await self.repository.save(record)
        return PhysicalRecordResponse.model_validate(saved_record)
