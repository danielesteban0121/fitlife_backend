from decimal import ROUND_HALF_UP, Decimal
from typing import Any, Dict, List, Optional

from src.domain.entities.assessment import ActivityLevel, Assessment, ExperienceLevel
from src.domain.entities.assessment_question import AssessmentQuestion, QuestionCategory
from src.domain.enums.fitness_level import FitnessLevel


class AssessmentCalculator:
    """
    Servicio de Dominio encargado de calcular el 'fitness_score' (0-100)
    y la 'body_age' (edad corporal estimada) de un usuario.

    Soporta dos modos de cálculo:
    1. Modo simplificado: usa los datos directos del Assessment (actividad, experiencia, BMI).
    2. Modo ponderado: usa respuestas a preguntas con pesos definidos (AssessmentQuestion).
    """

    # ─── Modo Simplificado ──────────────────────────────────────────────────

    def calculate_score(self, assessment: Assessment) -> float:
        """
        Calcula el fitness_score base (modo simplificado).
        Mantiene compatibilidad con las pruebas unitarias existentes.
        """
        base_score = Decimal("50.0")

        # Ajuste por nivel de actividad
        activity_adjustments: Dict[ActivityLevel, Decimal] = {
            ActivityLevel.SEDENTARY: Decimal("-10.0"),
            ActivityLevel.LIGHTLY_ACTIVE: Decimal("0.0"),
            ActivityLevel.MODERATELY_ACTIVE: Decimal("10.0"),
            ActivityLevel.VERY_ACTIVE: Decimal("20.0"),
            ActivityLevel.EXTRA_ACTIVE: Decimal("25.0"),
        }
        base_score += activity_adjustments.get(assessment.activity_level, Decimal("0"))

        # Ajuste por nivel de experiencia
        experience_adjustments: Dict[ExperienceLevel, Decimal] = {
            ExperienceLevel.BEGINNER: Decimal("-5.0"),
            ExperienceLevel.INTERMEDIATE: Decimal("10.0"),
            ExperienceLevel.ADVANCED: Decimal("20.0"),
        }
        base_score += experience_adjustments.get(
            assessment.experience_level, Decimal("0")
        )

        # Ajuste por IMC
        base_score += self._bmi_adjustment(assessment.height_cm, assessment.weight_kg)

        # Límites 1-100
        result = max(Decimal("1.0"), min(Decimal("100.0"), base_score))
        return float(result)

    # ─── Modo Ponderado ─────────────────────────────────────────────────────

    def calculate_weighted_score(
        self,
        responses: Dict[str, Any],
        questions: List[AssessmentQuestion],
    ) -> float:
        """
        Calcula el fitness_score ponderado a partir de respuestas a preguntas.

        Args:
            responses: Mapa {question_id: answer_value}
            questions: Lista de preguntas con sus pesos

        Returns:
            float: Puntaje entre 0.0 y 100.0
        """
        questions_map = {str(q.id): q for q in questions if q.is_active}

        total_weight = Decimal("0")
        weighted_sum = Decimal("0")

        for question_id, answer in responses.items():
            question = questions_map.get(question_id)
            if not question:
                continue

            weight = Decimal(str(question.weight))
            normalized_score = self._normalize_answer(answer, question)

            weighted_sum += normalized_score * weight
            total_weight += weight

        if total_weight == Decimal("0"):
            return 0.0

        score = (weighted_sum / total_weight * Decimal("100")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        return float(max(Decimal("0"), min(Decimal("100"), score)))

    # ─── Cálculo de Body Age ────────────────────────────────────────────────

    def calculate_body_age(
        self,
        real_age: int,
        height_cm: float,
        weight_kg: float,
        body_fat_percentage: Optional[float],
        fitness_score: float,
    ) -> float:
        """
        Estima la edad corporal (body age) del usuario.

        Una edad corporal menor que la real indica buena salud;
        mayor indica deterioro funcional.

        Returns:
            float: Edad corporal estimada (mínimo 10, máximo 120).
        """
        body_age = Decimal(str(real_age))

        # Ajuste por IMC
        body_age += self._bmi_adjustment(height_cm, weight_kg)

        # Ajuste por porcentaje de grasa corporal
        if body_fat_percentage is not None:
            body_age += self._fat_adjustment(body_fat_percentage, real_age)

        # Ajuste inverso por nivel de fitness: mejor fitness → menor edad corporal
        fitness_adj = Decimal(str(fitness_score - 50)) * Decimal("-0.1")
        body_age += fitness_adj

        # Límites razonables
        return float(
            max(Decimal("10"), min(Decimal("120"), body_age)).quantize(
                Decimal("0.1"), rounding=ROUND_HALF_UP
            )
        )

    # ─── Categorización ─────────────────────────────────────────────────────

    @staticmethod
    def categorize(fitness_score: float) -> FitnessLevel:
        """Determina la categoría de fitness según el puntaje."""
        if fitness_score >= 80:
            return FitnessLevel.EXCELLENT
        if fitness_score >= 60:
            return FitnessLevel.GOOD
        if fitness_score >= 40:
            return FitnessLevel.FAIR
        return FitnessLevel.POOR

    # ─── Helpers privados ───────────────────────────────────────────────────

    def _bmi_adjustment(self, height_cm: float, weight_kg: float) -> Decimal:
        """Penalización según el IMC del usuario."""
        if height_cm <= 0:
            return Decimal("0")

        height_m = height_cm / 100.0
        bmi = weight_kg / (height_m ** 2)

        if bmi < 18.5:
            return Decimal("-5.0")
        if bmi < 25.0:
            return Decimal("0.0")
        if bmi < 30.0:
            return Decimal("-5.0")
        return Decimal("-10.0")

    def _fat_adjustment(self, body_fat: float, age: int) -> Decimal:
        """
        Ajusta la edad corporal según el porcentaje de grasa.
        Los rangos saludables varían con la edad.
        """
        healthy_max = 20.0 if age < 40 else 25.0

        if body_fat <= healthy_max:
            return Decimal("-2.0")  # Grasa óptima → más joven
        if body_fat <= healthy_max + 10:
            return Decimal("2.0")  # Sobrepeso leve
        return Decimal("5.0")  # Obesidad

    @staticmethod
    def _normalize_answer(answer: Any, question: AssessmentQuestion) -> Decimal:
        """
        Normaliza una respuesta a un valor entre 0.0 y 1.0
        para el cálculo ponderado.
        """
        from src.domain.entities.assessment_question import QuestionType

        if question.question_type == QuestionType.YES_NO:
            return Decimal("1.0") if answer is True else Decimal("0.0")

        if question.question_type == QuestionType.NUMERIC:
            min_val = Decimal(str(question.constraints.get("min", 0)))
            max_val = Decimal(str(question.constraints.get("max", 10)))
            value = Decimal(str(answer))
            if max_val == min_val:
                return Decimal("0")
            normalized = (value - min_val) / (max_val - min_val)
            return max(Decimal("0"), min(Decimal("1"), normalized))

        if question.question_type == QuestionType.SINGLE_CHOICE:
            # Se asume que las opciones están ordenadas de peor a mejor
            if question.options and answer in question.options:
                idx = question.options.index(answer)
                return Decimal(str(idx)) / Decimal(str(len(question.options) - 1))
            return Decimal("0")

        if question.question_type == QuestionType.MULTIPLE_CHOICE:
            if not question.options or not isinstance(answer, list):
                return Decimal("0")
            selected = len([a for a in answer if a in question.options])
            return Decimal(str(selected)) / Decimal(str(len(question.options)))

        return Decimal("0")
