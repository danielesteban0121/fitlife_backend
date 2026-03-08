import pytest

from src.domain.entities.assessment import (
    ActivityLevel,
    Assessment,
    ExperienceLevel,
    FitnessGoal,
)
from src.domain.services.assessment_calculator import AssessmentCalculator


@pytest.fixture
def calculator():
    return AssessmentCalculator()


def test_calculate_score_very_active_advanced(calculator):
    assessment = Assessment(
        id="abc",
        user_id="user-1",
        goal=FitnessGoal.MUSCLE_GAIN,
        activity_level=ActivityLevel.VERY_ACTIVE,
        experience_level=ExperienceLevel.ADVANCED,
        height_cm=175.0,
        weight_kg=70.0,
        age=25,
    )
    score = calculator.calculate_score(assessment)
    assert score > 0
    assert score <= 100
    # 50 (base) + 20 (very_active) + 20 (advanced) = 90, sin penalización de IMC
    assert score == pytest.approx(90.0)


def test_calculate_score_sedentary_beginner(calculator):
    assessment = Assessment(
        id="def",
        user_id="user-2",
        goal=FitnessGoal.WEIGHT_LOSS,
        activity_level=ActivityLevel.SEDENTARY,
        experience_level=ExperienceLevel.BEGINNER,
        height_cm=170.0,
        weight_kg=65.0,
        age=30,
    )
    score = calculator.calculate_score(assessment)
    # 50 - 10 (sedentary) - 5 (beginner) = 35
    assert score == pytest.approx(35.0)


def test_calculate_score_clamped_to_min(calculator):
    """Score nunca baja de 1.0"""
    assessment = Assessment(
        id="ghi",
        user_id="user-3",
        goal=FitnessGoal.GENERAL_HEALTH,
        activity_level=ActivityLevel.SEDENTARY,
        experience_level=ExperienceLevel.BEGINNER,
        height_cm=160.0,
        weight_kg=120.0,  # BMI alto -> penalización extra
        age=40,
    )
    score = calculator.calculate_score(assessment)
    assert score >= 1.0
    assert score <= 100.0
