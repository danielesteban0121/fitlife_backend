from dataclasses import dataclass

from ..exceptions.validation_exceptions import InvalidValueException


@dataclass(frozen=True)
class FitnessScore:
    """
    Value Object para el puntaje de fitness (0.0 – 100.0).

    Encapsula el resultado de la evaluación física y garantiza
    que siempre esté en un rango válido.
    """

    value: float

    def __post_init__(self):
        if not (0.0 <= self.value <= 100.0):
            raise InvalidValueException(
                f"FitnessScore fuera del rango 0-100: {self.value}"
            )

    @property
    def is_excellent(self) -> bool:
        return self.value >= 80.0

    @property
    def is_good(self) -> bool:
        return 60.0 <= self.value < 80.0

    @property
    def is_fair(self) -> bool:
        return 40.0 <= self.value < 60.0

    @property
    def is_poor(self) -> bool:
        return self.value < 40.0

    def __str__(self) -> str:
        return f"{self.value:.2f}/100"
