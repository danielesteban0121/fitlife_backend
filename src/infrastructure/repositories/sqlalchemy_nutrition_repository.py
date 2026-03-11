from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.domain.entities.nutrition import NutritionPlan
from src.domain.repositories.nutrition_repository import NutritionRepository
from src.infrastructure.database.models.nutrition_models import NutritionPlanModel
from src.infrastructure.mappers.nutrition_mapper import NutritionMapper


class SQLAlchemyNutritionRepository(NutritionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_plan(self, plan: NutritionPlan) -> NutritionPlan:
        model = NutritionMapper.plan_to_model(plan)

        for meal_domain in plan.meals:
            meal_model = NutritionMapper.meal_to_model(meal_domain, plan_id=str(plan.id))
            model.meals.append(meal_model)

        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return NutritionMapper.plan_to_domain(model)

    async def find_plan_by_id(self, plan_id: UUID) -> Optional[NutritionPlan]:
        result = await self.session.execute(
            select(NutritionPlanModel)
            .options(selectinload(NutritionPlanModel.meals))
            .where(NutritionPlanModel.id == str(plan_id))
        )
        model = result.scalar_one_or_none()
        return NutritionMapper.plan_to_domain(model) if model else None

    async def get_active_plan_by_user(self, user_id: UUID) -> Optional[NutritionPlan]:
        result = await self.session.execute(
            select(NutritionPlanModel)
            .options(selectinload(NutritionPlanModel.meals))
            .where(NutritionPlanModel.user_id == str(user_id))
            .where(NutritionPlanModel.is_active.is_(True))
        )
        model = result.scalar_one_or_none()
        return NutritionMapper.plan_to_domain(model) if model else None

    async def find_active_by_user_id(self, user_id: UUID) -> Optional[NutritionPlan]:
        return await self.get_active_plan_by_user(user_id)
