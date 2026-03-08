import pytest

from src.application.dtos.assessment_dtos import (
    SubmitAssessmentDTO,
    AnswerDTO,
)
from src.application.use_cases.assessments.submit_assessment_use_case import (
    SubmitAssessmentUseCase,
)


class FakeAssessmentRepository:

    async def save(self, assessment):
        return assessment


@pytest.mark.asyncio
async def test_submit_assessment_use_case():

    repo = FakeAssessmentRepository()

    use_case = SubmitAssessmentUseCase(repo)

    dto = SubmitAssessmentDTO(
        user_id=1,
        answers=[
            AnswerDTO(question_id=1, answer=5),
            AnswerDTO(question_id=2, answer=4),
        ],
    )

    result = await use_case.execute(dto)

    assert result.user_id == 1
    assert result.fitness_score > 0
