from uuid import uuid4

from src.domain.entities.assessment import Assessment, FitnessGoal, ActivityLevel, ExperienceLevel
from src.domain.repositories.assessment_repository import AssessmentRepository
from src.domain.services.assessment_calculator import AssessmentCalculator

from src.application.dtos.assessment_dtos import SubmitAssessmentRequest, AssessmentResponse


class SubmitAssessment:
    def __init__(
        self,
        repository: AssessmentRepository,
        calculator: AssessmentCalculator,
    ):
        self.repository = repository
        self.calculator = calculator

    async def execute(self, user_id: str, request: SubmitAssessmentRequest) -> AssessmentResponse:

        # 1. Crear la entidad de Assessment
        assessment = Assessment(
            id=str(uuid4()),
            user_id=user_id,
            goal=FitnessGoal(request.goal),
            activity_level=ActivityLevel(request.activity_level),
            experience_level=ExperienceLevel(request.experience_level),
            height_cm=request.height_cm,
            weight_kg=request.weight_kg,
            age=request.age,
        )

        # 2. Calcular el score asignado por la calculadora de dominio
        assessment.fitness_score = self.calculator.calculate_score(assessment)

        # 3. Guardar o actualizar en base de datos
        # (Si ya existe, se sobrescribirá gracias a la lógica del repositorio)
        saved_assessment = await self.repository.save(assessment)

        # 4. Devolver la respuesta en formato DTO
        return AssessmentResponse(
            id=saved_assessment.id,
            user_id=saved_assessment.user_id,
            goal=saved_assessment.goal,
            activity_level=saved_assessment.activity_level,
            experience_level=saved_assessment.experience_level,
            height_cm=saved_assessment.height_cm,
            weight_kg=saved_assessment.weight_kg,
            age=saved_assessment.age,
            fitness_score=saved_assessment.fitness_score,
            created_at=saved_assessment.created_at,
        )
