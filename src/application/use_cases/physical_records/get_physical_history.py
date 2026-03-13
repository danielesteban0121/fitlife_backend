from typing import List
from uuid import UUID

from src.application.dtos.physical_record_dtos import PhysicalRecordResponse
from src.domain.repositories.physical_record_repository import PhysicalRecordRepository


class GetPhysicalHistory:
    """Caso de uso para recuperar el historial de mediciones de un usuario."""

    def __init__(self, repository: PhysicalRecordRepository):
        self.repository = repository

    async def execute(self, user_id: UUID) -> List[PhysicalRecordResponse]:
        records = await self.repository.find_by_user_id(user_id)
        return [PhysicalRecordResponse.model_validate(r) for r in records]
