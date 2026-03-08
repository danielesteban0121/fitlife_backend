import pytest

from src.application.dtos.assessment_dtos import SubmitAssessmentRequest
from src.application.use_cases.assessments.submit_assessment import SubmitAssessment
from src.domain.entities.assessment import Assessment, FitnessGoal
from src.domain.services.assessment_calculator import AssessmentCalculator


class FakeAssessmentRepository:
    async def save(self, assessment: Assessment) -> Assessment:
        return assessment

    async def find_by_user_id(self, user_id: str):
        return None

    async def delete_by_user_id(self, user_id: str) -> None:
        pass


@pytest.mark.asyncio
async def test_submit_assessment_use_case():
    repo = FakeAssessmentRepository()
    calculator = AssessmentCalculator()
    use_case = SubmitAssessment(repo, calculator)

    request = SubmitAssessmentRequest(
        goal="muscle_gain",
        activity_level="very_active",
        experience_level="intermediate",
        height_cm=175.0,
        weight_kg=70.0,
        age=25,
    )

    result = await use_case.execute(user_id="user-123", request=request)

    assert result.user_id == "user-123"
    assert result.fitness_score is not None
    assert result.fitness_score > 0
    assert result.goal == FitnessGoal.MUSCLE_GAIN
