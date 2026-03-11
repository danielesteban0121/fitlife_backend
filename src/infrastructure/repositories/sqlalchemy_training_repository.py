from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.domain.entities.training import Exercise, Routine, WorkoutLog
from src.domain.repositories.training_repository import TrainingRepository
from src.infrastructure.database.models.training_models import (
    ExerciseModel,
    RoutineModel,
    WorkoutLogModel,
)
from src.infrastructure.mappers.training_mapper import TrainingMapper


class SQLAlchemyTrainingRepository(TrainingRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_routine(self, routine: Routine) -> Routine:
        model = TrainingMapper.routine_to_model(routine)

        for ex_domain in routine.exercises:
            ex_model = TrainingMapper.routine_exercise_to_model(
                ex_domain, routine_id=str(routine.id)
            )
            model.exercises.append(ex_model)

        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return TrainingMapper.routine_to_domain(model)

    async def find_routine_by_id(self, routine_id: UUID) -> Optional[Routine]:
        result = await self.session.execute(
            select(RoutineModel)
            .options(selectinload(RoutineModel.exercises))
            .where(RoutineModel.id == str(routine_id))
        )
        model = result.scalar_one_or_none()
        return TrainingMapper.routine_to_domain(model) if model else None

    async def get_routines_by_user(self, user_id: UUID) -> List[Routine]:
        result = await self.session.execute(
            select(RoutineModel)
            .options(selectinload(RoutineModel.exercises))
            .where(RoutineModel.user_id == str(user_id))
        )
        models = result.scalars().all()
        return [TrainingMapper.routine_to_domain(m) for m in models]

    async def get_all_exercises(self) -> List[Exercise]:
        result = await self.session.execute(select(ExerciseModel))
        models = result.scalars().all()
        return [TrainingMapper.exercise_to_domain(m) for m in models]

    async def save_workout_log(self, log: WorkoutLog) -> WorkoutLog:
        model = TrainingMapper.workout_log_to_model(log)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return TrainingMapper.workout_log_to_domain(model)

    async def get_workout_history(self, user_id: UUID) -> List[WorkoutLog]:
        result = await self.session.execute(
            select(WorkoutLogModel)
            .where(WorkoutLogModel.user_id == str(user_id))
            .order_by(WorkoutLogModel.completed_at.desc())
        )
        models = result.scalars().all()
        return [TrainingMapper.workout_log_to_domain(m) for m in models]

    async def assign_routine(self, user_id: UUID, routine_id: UUID) -> bool:
        # En una arquitectura real, esto podría actualizar una tabla de relación
        # o un campo en UserProfile. Por ahora simplificamos.
        return True
