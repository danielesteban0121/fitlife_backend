from decimal import Decimal

import pytest

from src.domain.exceptions.validation_exceptions import InvalidBMIException
from src.domain.services.bmi_calculator import BMICalculator


def test_bmi_calculation():
    bmi = BMICalculator.calculate(Decimal("70"), Decimal("1.75"))
    assert bmi == Decimal("22.86")


def test_bmi_invalid_height():
    with pytest.raises(InvalidBMIException):
        BMICalculator.calculate(Decimal("70"), Decimal("0"))
