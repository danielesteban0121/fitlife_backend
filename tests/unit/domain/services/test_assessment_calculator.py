import pytest
from src.domain.entities.assessment import Assessment, FitnessGoal, ActivityLevel, ExperienceLevel
from src.domain.services.assessment_calculator import AssessmentCalculator


def test_base_calculation_with_sedentary_beginner():
    calc = AssessmentCalculator()

    assessment = Assessment(
        id="a1",
        user_id="u1",
        goal=FitnessGoal.WEIGHT_LOSS,
        activity_level=ActivityLevel.SEDENTARY,
        experience_level=ExperienceLevel.BEGINNER,
        height_cm=170,
        weight_kg=70,  # BMI normal (24.22)
        age=30,
    )

    score = calc.calculate_score(assessment)
    # Base 50 - 10 (Sedentary) - 5 (Beginner) = 35.0
    assert score == 35.0


def test_calculation_with_advanced_extra_active():
    calc = AssessmentCalculator()

    assessment = Assessment(
        id="a2",
        user_id="u2",
        goal=FitnessGoal.MUSCLE_GAIN,
        activity_level=ActivityLevel.EXTRA_ACTIVE,
        experience_level=ExperienceLevel.ADVANCED,
        height_cm=180,
        weight_kg=80,  # BMI normal (24.69)
        age=25,
    )

    score = calc.calculate_score(assessment)
    # Base 50 + 25 (Extra Active) + 20 (Advanced) = 95.0
    assert score == 95.0


def test_calculation_with_obese_bmi_penalty():
    calc = AssessmentCalculator()

    assessment = Assessment(
        id="a3",
        user_id="u3",
        goal=FitnessGoal.WEIGHT_LOSS,
        activity_level=ActivityLevel.MODERATELY_ACTIVE,
        experience_level=ExperienceLevel.INTERMEDIATE,
        height_cm=160,
        weight_kg=90,  # BMI > 35 (Obese)
        age=45,
    )

    score = calc.calculate_score(assessment)
    # Base 50 + 10 (ModActive) + 10 (Interm) = 70
    # BMI > 30 -> penalty -10 -> 60.0
    assert score == 60.0


def test_score_max_cap():
    calc = AssessmentCalculator()

    # Incluso con bonos altos, no debería pasar 100
    assessment = Assessment(
        id="a4",
        user_id="u4",
        goal=FitnessGoal.ENDURANCE,
        activity_level=ActivityLevel.EXTRA_ACTIVE,  # +25
        experience_level=ExperienceLevel.ADVANCED,  # +20
        height_cm=190,
        weight_kg=85,  # Normal BMI
        age=22,
    )

    score = calc.calculate_score(assessment)
    assert score == 95.0
