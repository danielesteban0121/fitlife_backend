from fastapi import APIRouter, Depends

from src.adapters.api.dependencies import get_submit_assessment_use_case
from src.application.use_cases.assessments.submit_assessment_use_case import SubmitAssessmentUseCase

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
    use_case: SubmitAssessmentUseCase = Depends(get_submit_assessment_use_case),
):

    dto = SubmitAssessmentDTO(
        user_id=payload.user_id,
        answers=[AnswerDTO(**a.model_dump()) for a in payload.answers],
    )

    result = await use_case.execute(dto)

    return {
        "assessment_id": result.id,
        "fitness_score": result.fitness_score,
    }
