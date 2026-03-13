from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from src.application.use_cases.assessments.get_assessment_questions import GetAssessmentQuestions
from src.domain.entities.assessment_question import AssessmentQuestion, QuestionCategory, QuestionType


@pytest.mark.asyncio
async def test_get_assessment_questions_success():
    # Arrange
    repository = MagicMock()
    repository.find_questions = AsyncMock()
    use_case = GetAssessmentQuestions(repository)
    
    questions = [
        AssessmentQuestion(
            id=uuid4(), 
            question_type=QuestionType.NUMERIC, 
            category=QuestionCategory.PHYSICAL, 
            label="¿Cuál es tu peso?"
        ),
        AssessmentQuestion(
            id=uuid4(), 
            question_type=QuestionType.YES_NO, 
            category=QuestionCategory.HABITS, 
            label="¿Fumas?"
        ),
    ]
    repository.find_questions.return_value = questions

    # Act
    result = await use_case.execute()

    # Assert
    assert len(result) == 2
    assert result[0].label == "¿Cuál es tu peso?"
    repository.find_questions.assert_called_once_with(None)


@pytest.mark.asyncio
async def test_get_assessment_questions_by_category():
    # Arrange
    repository = MagicMock()
    repository.find_questions = AsyncMock()
    use_case = GetAssessmentQuestions(repository)
    
    repository.find_questions.return_value = []

    # Act
    await use_case.execute(QuestionCategory.PHYSICAL)

    # Assert
    repository.find_questions.assert_called_once_with(QuestionCategory.PHYSICAL)
