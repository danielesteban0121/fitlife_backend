from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Optional
from uuid import UUID


@dataclass
class PhysicalRecord:
    """
    Registro físico periódico de un usuario.

    Almacena medidas corporales en un momento dado para
    poder hacer seguimiento del progreso a lo largo del tiempo.
    """

    id: UUID
    user_id: UUID
    weight_kg: float
    height_cm: float
    body_fat_percentage: Optional[float] = None
    muscle_mass_kg: Optional[float] = None
    waist_cm: Optional[float] = None
    chest_cm: Optional[float] = None
    hips_cm: Optional[float] = None
    notes: Optional[str] = None
    recorded_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @property
    def bmi(self) -> Optional[float]:
        """Calcula el IMC a partir del peso y la altura."""
        if self.height_cm and self.height_cm > 0:
            height_m = self.height_cm / 100.0
            return round(self.weight_kg / (height_m ** 2), 2)
        return None

    @property
    def bmi_category(self) -> str:
        """Categoría de IMC según la OMS."""
        bmi_value = self.bmi
        if bmi_value is None:
            return "Unknown"
        if bmi_value < 18.5:
            return "Underweight"
        if bmi_value < 25.0:
            return "Normal"
        if bmi_value < 30.0:
            return "Overweight"
        return "Obese"
