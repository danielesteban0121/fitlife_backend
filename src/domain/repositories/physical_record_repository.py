from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ..entities.physical_record import PhysicalRecord


class PhysicalRecordRepository(ABC):
    """Puerto de salida para persistencia de registros físicos."""

    @abstractmethod
    async def save(self, record: PhysicalRecord) -> PhysicalRecord:
        """Persiste un nuevo registro físico."""
        pass

    @abstractmethod
    async def find_by_user_id(
        self,
        user_id: UUID,
        limit: Optional[int] = None,
    ) -> List[PhysicalRecord]:
        """Retorna el historial de registros físicos de un usuario, ordenado descendientemente por fecha."""
        pass

    @abstractmethod
    async def find_latest_by_user_id(self, user_id: UUID) -> Optional[PhysicalRecord]:
        """Retorna el registro físico más reciente del usuario."""
        pass

    @abstractmethod
    async def find_by_id(self, record_id: UUID) -> Optional[PhysicalRecord]:
        """Busca un registro específico por su ID."""
        pass

    @abstractmethod
    async def delete(self, record_id: UUID) -> None:
        """Elimina un registro físico por su ID."""
        pass
