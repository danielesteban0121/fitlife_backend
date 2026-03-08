from src.domain.entities.assessment import Assessment, ActivityLevel, ExperienceLevel, FitnessGoal


class AssessmentCalculator:
    """
    Servicio de Dominio encargado de calcular un 'fitness_score' base
    (del 1 al 100) en base a la información provista por el usuario.
    """

    def calculate_score(self, assessment: Assessment) -> float:
        base_score = 50.0  # Puntaje base medio

        # Ajuste por nivel de actividad
        activity_multipliers = {
            ActivityLevel.SEDENTARY: -10.0,
            ActivityLevel.LIGHTLY_ACTIVE: 0.0,
            ActivityLevel.MODERATELY_ACTIVE: +10.0,
            ActivityLevel.VERY_ACTIVE: +20.0,
            ActivityLevel.EXTRA_ACTIVE: +25.0,
        }
        base_score += activity_multipliers.get(assessment.activity_level, 0.0)

        # Ajuste por nivel de experiencia
        experience_multipliers = {
            ExperienceLevel.BEGINNER: -5.0,
            ExperienceLevel.INTERMEDIATE: +10.0,
            ExperienceLevel.ADVANCED: +20.0,
        }
        base_score += experience_multipliers.get(assessment.experience_level, 0.0)

        # Ajuste simple por IMC (Índice de Masa Corporal)
        if assessment.height_cm > 0:
            height_m = assessment.height_cm / 100.0
            bmi = assessment.weight_kg / (height_m * height_m)

            if bmi < 18.5:
                base_score -= 5.0
            elif 25.0 <= bmi < 30.0:
                base_score -= 5.0
            elif bmi >= 30.0:
                base_score -= 10.0

        # Aseguramos límites
        return max(1.0, min(100.0, base_score))
