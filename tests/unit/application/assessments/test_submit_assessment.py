import pytest
from unittest.mock import AsyncMock, Mock, patch

from src.application.use_cases.assessments.submit_assessment import SubmitAssessment
from src.application.dtos.assessment_dtos import SubmitAssessmentRequest
from src.domain.entities.assessment import Assessment, FitnessGoal, ActivityLevel, ExperienceLevel


@pytest.mark.asyncio
async def test_submit_assessment_success():
    mock_repo = AsyncMock()
    mock_calc = Mock()

    # La calculadora retorna un score fijo en el mock
    mock_calc.calculate_score.return_value = 85.0

    # Configuración del repositorio
    async def mock_save(assessment: Assessment):
        # Repositorio mutado o devuelto tal cual
        return assessment

    mock_repo.save = AsyncMock(side_effect=mock_save)

    use_case = SubmitAssessment(
        repository=mock_repo,
        calculator=mock_calc,
    )

    request = SubmitAssessmentRequest(
        goal=FitnessGoal.MUSCLE_GAIN,
        activity_level=ActivityLevel.MODERATELY_ACTIVE,
        experience_level=ExperienceLevel.INTERMEDIATE,
        height_cm=175.0,
        weight_kg=75.0,
        age=28,
    )

    response = await use_case.execute(user_id="test-user-123", request=request)

    assert response.user_id == "test-user-123"
    assert response.fitness_score == 85.0
    assert response.goal == FitnessGoal.MUSCLE_GAIN

    # Confirmar interacciones
    mock_calc.calculate_score.assert_called_once()
    mock_repo.save.assert_called_once()
