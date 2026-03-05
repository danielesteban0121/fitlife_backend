from abc import ABC
from abc import abstractmethod

from src.domain.entities.assessment import Assessment


class AssessmentRepository(ABC):

    @abstractmethod
    async def save(self, assessment: Assessment):
        pass
