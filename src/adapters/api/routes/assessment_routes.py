from typing import Any, Dict

from fastapi import APIRouter, Depends

from src.adapters.api.dependencies import get_current_user, get_submit_assessment
from src.application.dtos.assessment_dtos import AssessmentResponse, SubmitAssessmentRequest
from src.application.use_cases.assessments.submit_assessment import SubmitAssessment

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
