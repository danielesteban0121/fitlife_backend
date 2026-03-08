<<<<<<< HEAD
from abc import ABC
from abc import abstractmethod

=======
from abc import ABC, abstractmethod
from typing import Optional
>>>>>>> a8a4ebf (feat(auth,assessment): implementar flujo completo de autenticación JWT y módulo de valoraciones físicas)
from src.domain.entities.assessment import Assessment


class AssessmentRepository(ABC):
<<<<<<< HEAD

    @abstractmethod
    async def save(self, assessment: Assessment):
=======
    
    @abstractmethod
    async def save(self, assessment: Assessment) -> Assessment:
        pass

    @abstractmethod
    async def find_by_user_id(self, user_id: str) -> Optional[Assessment]:
        pass

    @abstractmethod
    async def delete_by_user_id(self, user_id: str) -> None:
>>>>>>> a8a4ebf (feat(auth,assessment): implementar flujo completo de autenticación JWT y módulo de valoraciones físicas)
        pass
