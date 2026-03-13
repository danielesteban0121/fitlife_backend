from enum import Enum


class FitnessLevel(str, Enum):
    """Nivel de aptitud física del usuario (calculado tras evaluación)."""

    EXCELLENT = "EXCELLENT"
    GOOD = "GOOD"
    FAIR = "FAIR"
    POOR = "POOR"
