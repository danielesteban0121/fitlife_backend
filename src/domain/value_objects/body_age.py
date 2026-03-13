from dataclasses import dataclass

from ..exceptions.validation_exceptions import InvalidValueException


@dataclass(frozen=True)
class BodyAge:
    """
    Value Object para la edad corporal estimada.

    La edad corporal puede diferir de la edad cronológica
    dependiendo del nivel de fitness y hábitos de vida.

    Rango válido: 10 – 120 años.
    """

    value: float

    def __post_init__(self):
        if not (10.0 <= self.value <= 120.0):
            raise InvalidValueException(
                f"BodyAge fuera del rango válido (10-120): {self.value}"
            )

    def age_difference(self, real_age: int) -> float:
        """
        Diferencia entre la edad corporal y la cronológica.
        Negativo → 'más joven' de lo que indica la edad real.
        Positivo → 'más viejo'.
        """
        return round(self.value - real_age, 1)

    def __str__(self) -> str:
        return f"{self.value:.1f} años"
