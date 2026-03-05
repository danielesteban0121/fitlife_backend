from fastapi import APIRouter
from fastapi import Depends

from src.adapters.api.schemas.assessment_schemas import (
    SubmitAssessmentSchema,
)
from src.application.dtos.assessment_dtos import (
    SubmitAssessmentDTO,
    AnswerDTO,
)
from src.application.use_cases.assessments.submit_assessment_use_case import (
    SubmitAssessmentUseCase,
)
from src.infrastructure.repositories.sqlalchemy_assessment_repository import (
    SQLAlchemyAssessmentRepository,
)
from src.infrastructure.database.connection import get_session


router = APIRouter(prefix="/api/assessments", tags=["assessments"])


@router.post("/submit")
async def submit_assessment(
    payload: SubmitAssessmentSchema,
    session=Depends(get_session),
):

    repo = SQLAlchemyAssessmentRepository(session)

    use_case = SubmitAssessmentUseCase(repo)

    dto = SubmitAssessmentDTO(
        user_id=payload.user_id,
        answers=[AnswerDTO(**answer.model_dump()) for answer in payload.answers],
    )

    result = await use_case.execute(dto)

    return {
        "assessment_id": result.id,
        "fitness_score": result.fitness_score,
    }
