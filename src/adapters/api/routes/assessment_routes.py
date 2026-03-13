"""Rutas de evaluación física: enviar evaluación e historial."""
from typing import Any, Dict, List

from fastapi import APIRouter, Depends

from src.adapters.api.dependencies import get_current_user, get_submit_assessment
from src.adapters.api.dependencies_phase_f import (
    get_get_assessment_history,
    get_get_assessment_questions,
)

from src.application.dtos.assessment_dtos import AssessmentResponse, SubmitAssessmentRequest
from src.application.use_cases.assessments.submit_assessment import SubmitAssessment

router = APIRouter(prefix="/api/assessments", tags=["Assessments"])


@router.post("/submit", response_model=AssessmentResponse, status_code=201)
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


@router.get("/history", response_model=List[AssessmentResponse])
async def get_assessment_history(
    current_user: Dict[str, Any] = Depends(get_current_user),
    use_case=Depends(get_get_assessment_history),
):
    """Retorna el historial de evaluaciones físicas del usuario autenticado."""
    user_id = current_user["user_id"]
    return await use_case.execute(user_id=user_id)


@router.get("/questions", response_model=List[Dict[str, Any]])
async def get_assessment_questions(
    use_case=Depends(get_get_assessment_questions),
):
    """Retorna las preguntas configuradas para el cuestionario inicial."""
    questions = await use_case.execute()
    # Convertimos a dict para respuesta simple o usamos DTO
    return [
        {
            "id": str(q.id),
            "type": q.question_type.value,
            "category": q.category.value,
            "label": q.label,
            "options": q.options,
            "constraints": q.constraints,
        }
        for q in questions
    ]

