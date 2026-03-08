from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.assessment import Assessment


class AssessmentRepository(ABC):

    @abstractmethod
    async def save(self, assessment: Assessment) -> Assessment:
        pass

    @abstractmethod
    async def find_by_user_id(self, user_id: str) -> Optional[Assessment]:
        pass

    @abstractmethod
    async def delete_by_user_id(self, user_id: str) -> None:
        pass
