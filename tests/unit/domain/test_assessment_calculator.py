from src.domain.entities.assessment import AssessmentAnswer
from src.domain.services.assessment_calculator import (
    AssessmentCalculator,
)


def test_calculate_fitness_score():

    answers = [
        AssessmentAnswer(question_id=1, answer=5),
        AssessmentAnswer(question_id=2, answer=4),
        AssessmentAnswer(question_id=3, answer=3),
    ]

    score = AssessmentCalculator.calculate(answers)

    assert score > 0
    assert score <= 100
