from typing import Optional, List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.domain.entities.instructor import Instructor, InstructorAssignment
from src.domain.repositories.instructor_repository import InstructorRepository
from src.infrastructure.database.models.instructor_model import (
    InstructorModel,
    InstructorAssignmentModel,
)
from src.infrastructure.mappers.instructor_mapper import (
    InstructorMapper,
    InstructorAssignmentMapper,
)


class SQLAlchemyInstructorRepository(InstructorRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, instructor: Instructor) -> Instructor:
        model = InstructorMapper.to_model(instructor)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return InstructorMapper.to_domain(model)

    async def find_by_id(self, instructor_id: UUID) -> Optional[Instructor]:
        result = await self.session.execute(
            select(InstructorModel).where(InstructorModel.id == str(instructor_id))
        )
        model = result.scalar_one_or_none()
        return InstructorMapper.to_domain(model) if model else None

    async def find_by_user_id(self, user_id: UUID) -> Optional[Instructor]:
        result = await self.session.execute(
            select(InstructorModel).where(InstructorModel.user_id == str(user_id))
        )
        model = result.scalar_one_or_none()
        return InstructorMapper.to_domain(model) if model else None

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Instructor]:
        result = await self.session.execute(select(InstructorModel).offset(skip).limit(limit))
        models = result.scalars().all()
        return [InstructorMapper.to_domain(m) for m in models]

    async def save_assignment(self, assignment: InstructorAssignment) -> InstructorAssignment:
        model = InstructorAssignmentMapper.to_model(assignment)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return InstructorAssignmentMapper.to_domain(model)

    async def get_active_assignment_for_user(self, user_id: UUID) -> Optional[InstructorAssignment]:
        result = await self.session.execute(
            select(InstructorAssignmentModel)
            .where(InstructorAssignmentModel.user_id == str(user_id))
            .where(InstructorAssignmentModel.is_active == True)
        )
        model = result.scalar_one_or_none()
        return InstructorAssignmentMapper.to_domain(model) if model else None
