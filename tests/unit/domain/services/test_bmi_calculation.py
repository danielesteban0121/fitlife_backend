from decimal import Decimal
from src.domain.services.bmi_calculator import BMICalculator

def test_bmi_calculation():
    bmi = BMICalculator.calculate(Decimal("70"), Decimal("1.75"))
    assert bmi == Decimal("22.86")