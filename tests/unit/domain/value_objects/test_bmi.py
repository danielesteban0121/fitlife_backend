"""Tests unitarios para el Value Object BMI."""
import pytest

from src.domain.exceptions.validation_exceptions import InvalidValueException
from src.domain.value_objects.bmi import BMI


def test_bmi_from_measurements_normal():
    bmi = BMI.from_measurements(weight_kg=70, height_cm=170)
    assert 24.0 <= bmi.value <= 25.0


def test_bmi_category_underweight():
    bmi = BMI(value=17.5)
    assert bmi.category == "Underweight"


def test_bmi_category_normal():
    bmi = BMI(value=22.0)
    assert bmi.category == "Normal"


def test_bmi_category_overweight():
    bmi = BMI(value=27.0)
    assert bmi.category == "Overweight"


def test_bmi_category_obese():
    bmi = BMI(value=35.0)
    assert bmi.category == "Obese"


def test_bmi_invalid_too_low():
    with pytest.raises(InvalidValueException):
        BMI(value=5.0)


def test_bmi_invalid_too_high():
    with pytest.raises(InvalidValueException):
        BMI(value=80.0)


def test_bmi_invalid_zero_height():
    with pytest.raises(InvalidValueException):
        BMI.from_measurements(weight_kg=70, height_cm=0)


def test_bmi_str():
    bmi = BMI(value=22.5)
    assert "22.50" in str(bmi)
    assert "Normal" in str(bmi)
