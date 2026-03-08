<<<<<<< HEAD
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.assessment import Assessment
from src.domain.repositories.assessment_repository import (
    AssessmentRepository,
)
from src.infrastructure.database.models.assessment_model import (
    AssessmentModel,
)


class SQLAlchemyAssessmentRepository(AssessmentRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, assessment: Assessment):

        answers = [
            {
                "question_id": a.question_id,
                "answer": a.answer,
            }
            for a in assessment.answers
        ]

        model = AssessmentModel(
            user_id=assessment.user_id,
            fitness_score=assessment.fitness_score,
            answers=answers,
        )

        self.session.add(model)

        await self.session.commit()

        await self.session.refresh(model)

        return model
=======
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from src.domain.entities.assessment import Assessment
from src.domain.repositories.assessment_repository import AssessmentRepository
from src.infrastructure.database.models.assessment_model import AssessmentModel


class SQLAlchemyAssessmentRepository(AssessmentRepository):
    
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, assessment: Assessment) -> Assessment:
        # Verifica si existe y actualiza o inserta
        stmt = select(AssessmentModel).where(AssessmentModel.user_id == assessment.user_id)
        result = await self.session.execute(stmt)
        existing_model = result.scalar_one_or_none()

        if existing_model:
            existing_model.goal = assessment.goal
            existing_model.activity_level = assessment.activity_level
            existing_model.experience_level = assessment.experience_level
            existing_model.height_cm = assessment.height_cm
            existing_model.weight_kg = assessment.weight_kg
            existing_model.age = assessment.age
            existing_model.fitness_score = assessment.fitness_score
        else:
            model = AssessmentModel(
                id=assessment.id,
                user_id=assessment.user_id,
                goal=assessment.goal,
                activity_level=assessment.activity_level,
                experience_level=assessment.experience_level,
                height_cm=assessment.height_cm,
                weight_kg=assessment.weight_kg,
                age=assessment.age,
                fitness_score=assessment.fitness_score,
                created_at=assessment.created_at,
            )
            self.session.add(model)
            
        await self.session.commit()
        return assessment

    async def find_by_user_id(self, user_id: str) -> Optional[Assessment]:
        stmt = select(AssessmentModel).where(AssessmentModel.user_id == user_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if not model:
            return None
            
        return Assessment(
            id=model.id,
            user_id=model.user_id,
            goal=model.goal,
            activity_level=model.activity_level,
            experience_level=model.experience_level,
            height_cm=model.height_cm,
            weight_kg=model.weight_kg,
            age=model.age,
            fitness_score=model.fitness_score,
            created_at=model.created_at,
        )

    async def delete_by_user_id(self, user_id: str) -> None:
        stmt = delete(AssessmentModel).where(AssessmentModel.user_id == user_id)
        await self.session.execute(stmt)
        await self.session.commit()
>>>>>>> a8a4ebf (feat(auth,assessment): implementar flujo completo de autenticación JWT y módulo de valoraciones físicas)
