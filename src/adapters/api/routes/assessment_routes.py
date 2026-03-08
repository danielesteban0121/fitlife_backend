from fastapi import APIRouter, Depends
<<<<<<< HEAD

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
=======
from typing import Dict, Any

from src.application.dtos.assessment_dtos import SubmitAssessmentRequest, AssessmentResponse
from src.application.use_cases.assessments.submit_assessment import SubmitAssessment
from src.adapters.api.dependencies import get_submit_assessment, get_current_user

router = APIRouter(prefix="/api/assessments", tags=["Assessments"])


@router.post("/submit", response_model=AssessmentResponse)
async def submit_assessment(
    data: SubmitAssessmentRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    use_case: SubmitAssessment = Depends(get_submit_assessment),
):
    """
    Recibe la evaluación inicial de un usuario autenticado, evalúa su
    estado físico actual y guarda el Assessment en BD.
    """
    user_id = current_user["user_id"]
    return await use_case.execute(user_id=user_id, request=data)
>>>>>>> a8a4ebf (feat(auth,assessment): implementar flujo completo de autenticación JWT y módulo de valoraciones físicas)
