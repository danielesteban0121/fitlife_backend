from typing import List, Optional

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.assessment import Assessment
from src.domain.entities.assessment_question import AssessmentQuestion, QuestionCategory
from src.domain.repositories.assessment_repository import AssessmentRepository
from src.infrastructure.database.models.assessment_model import AssessmentModel
from src.infrastructure.database.models.assessment_question_model import AssessmentQuestionModel
from src.infrastructure.mappers.assessment_mapper import AssessmentMapper
from src.infrastructure.mappers.assessment_question_mapper import AssessmentQuestionMapper


class SQLAlchemyAssessmentRepository(AssessmentRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, assessment: Assessment) -> Assessment:
        model = AssessmentMapper.to_model(assessment)
        await self.session.merge(model)
        await self.session.commit()
        return assessment

    async def find_by_user_id(self, user_id: str) -> Optional[Assessment]:
        stmt = select(AssessmentModel).where(AssessmentModel.user_id == user_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return AssessmentMapper.to_domain(model) if model else None

    async def find_history_by_user_id(self, user_id: str) -> list[Assessment]:
        stmt = (
            select(AssessmentModel)
            .where(AssessmentModel.user_id == user_id)
            .order_by(AssessmentModel.created_at.desc())
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [AssessmentMapper.to_domain(m) for m in models]

    async def delete_by_user_id(self, user_id: str) -> None:
        stmt = delete(AssessmentModel).where(AssessmentModel.user_id == user_id)
        await self.session.execute(stmt)
        await self.session.commit()

    async def find_questions(
        self, category: Optional[QuestionCategory] = None
    ) -> List[AssessmentQuestion]:
        stmt = select(AssessmentQuestionModel).where(AssessmentQuestionModel.is_active == True)
        if category:
            stmt = stmt.where(AssessmentQuestionModel.category == category)
        
        stmt = stmt.order_by(AssessmentQuestionModel.display_order.asc())
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [AssessmentQuestionMapper.to_domain(m) for m in models]

    async def save_question(self, question: AssessmentQuestion) -> AssessmentQuestion:
        model = AssessmentQuestionMapper.to_model(question)
        await self.session.merge(model)
        await self.session.commit()
        return question
