"""Tests unitarios para AssessmentQuestion entity."""
from uuid import uuid4

import pytest

from src.domain.entities.assessment_question import (
    AssessmentQuestion,
    QuestionCategory,
    QuestionType,
)


@pytest.fixture
def yes_no_question():
    return AssessmentQuestion(
        id=uuid4(),
        question_type=QuestionType.YES_NO,
        category=QuestionCategory.HABITS,
        label="¿Realizas actividad física regularmente?",
    )


@pytest.fixture
def numeric_question():
    return AssessmentQuestion(
        id=uuid4(),
        question_type=QuestionType.NUMERIC,
        category=QuestionCategory.PHYSICAL,
        label="¿Cuántas horas duermes por noche?",
        weight=2.0,
        constraints={"min": 1, "max": 12},
    )


@pytest.fixture
def single_choice_question():
    return AssessmentQuestion(
        id=uuid4(),
        question_type=QuestionType.SINGLE_CHOICE,
        category=QuestionCategory.FUNCTIONAL,
        label="¿Cuál describe mejor tu dieta?",
        options=["Muy mala", "Mala", "Regular", "Buena", "Muy buena"],
    )


def test_yes_no_valid_true(yes_no_question):
    assert yes_no_question.validate_answer(True) is True


def test_yes_no_valid_false(yes_no_question):
    assert yes_no_question.validate_answer(False) is True


def test_yes_no_invalid_string(yes_no_question):
    assert yes_no_question.validate_answer("yes") is False


def test_numeric_valid_in_range(numeric_question):
    assert numeric_question.validate_answer(7) is True


def test_numeric_below_min(numeric_question):
    assert numeric_question.validate_answer(0) is False


def test_numeric_above_max(numeric_question):
    assert numeric_question.validate_answer(15) is False


def test_single_choice_valid(single_choice_question):
    assert single_choice_question.validate_answer("Buena") is True


def test_single_choice_invalid(single_choice_question):
    assert single_choice_question.validate_answer("Excelente") is False
