from dataclasses import dataclass

from ..exceptions.validation_exceptions import InvalidValueException


@dataclass(frozen=True)
class BMI:
    """
    Value Object para el Índice de Masa Corporal (IMC).
    
    Rango válido: 10.0 – 70.0 kg/m²
    """

    value: float

    def __post_init__(self):
        if not (10.0 <= self.value <= 70.0):
            raise InvalidValueException(f"IMC fuera de rango válido: {self.value}")

    @classmethod
    def from_measurements(cls, weight_kg: float, height_cm: float) -> "BMI":
        """Crea un BMI a partir del peso (kg) y la altura (cm)."""
        if height_cm <= 0:
            raise InvalidValueException("La altura debe ser mayor que 0.")
        height_m = height_cm / 100.0
        return cls(value=round(weight_kg / (height_m ** 2), 2))

    @property
    def category(self) -> str:
        """Categoría de IMC según la OMS."""
        if self.value < 18.5:
            return "Underweight"
        if self.value < 25.0:
            return "Normal"
        if self.value < 30.0:
            return "Overweight"
        return "Obese"

    def __str__(self) -> str:
        return f"{self.value:.2f} ({self.category})"
