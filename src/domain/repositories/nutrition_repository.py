from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from ..entities.nutrition import NutritionPlan


class NutritionRepository(ABC):
    """Puerto de salida para persistencia de planes de nutrición."""

    @abstractmethod
    async def save_plan(self, plan: NutritionPlan) -> NutritionPlan:
        pass

    @abstractmethod
    async def find_plan_by_id(self, plan_id: UUID) -> Optional[NutritionPlan]:
        pass

    @abstractmethod
    async def get_active_plan_by_user(self, user_id: UUID) -> Optional[NutritionPlan]:
        pass

    @abstractmethod
    async def find_active_by_user_id(self, user_id: UUID) -> Optional[NutritionPlan]:
        """Busca el plan activo de un usuario."""
