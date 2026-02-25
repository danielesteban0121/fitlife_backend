from decimal import Decimal

from ..exceptions.validation_exceptions import InvalidBMIException


class BMICalculator:

    @staticmethod
    def calculate(weight_kg: Decimal, height_m: Decimal) -> Decimal:
        if height_m <= 0:
            raise InvalidBMIException("Altura inválida")

        bmi = weight_kg / (height_m**2)
        return bmi.quantize(Decimal("0.01"))
