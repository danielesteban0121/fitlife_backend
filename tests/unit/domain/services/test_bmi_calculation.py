import pytest
from decimal import Decimal
from src.domain.services.bmi_calculator import BMICalculator
from src.domain.exceptions.validation_exceptions import InvalidBMIException


def test_bmi_calculation():
    bmi = BMICalculator.calculate(Decimal("70"), Decimal("1.75"))
    assert bmi == Decimal("22.86")


def test_bmi_invalid_height():
    with pytest.raises(InvalidBMIException):
        BMICalculator.calculate(Decimal("70"), Decimal("0"))
