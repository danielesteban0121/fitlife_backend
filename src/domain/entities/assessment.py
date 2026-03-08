<<<<<<< HEAD
from dataclasses import dataclass
from typing import List


@dataclass
class AssessmentAnswer:
    question_id: int
    answer: int
=======
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional


class FitnessGoal(str, Enum):
    WEIGHT_LOSS = "weight_loss"
    MUSCLE_GAIN = "muscle_gain"
    ENDURANCE = "endurance"
    FLEXIBILITY = "flexibility"
    GENERAL_HEALTH = "general_health"


class ActivityLevel(str, Enum):
    SEDENTARY = "sedentary"
    LIGHTLY_ACTIVE = "lightly_active"
    MODERATELY_ACTIVE = "moderately_active"
    VERY_ACTIVE = "very_active"
    EXTRA_ACTIVE = "extra_active"


class ExperienceLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
>>>>>>> a8a4ebf (feat(auth,assessment): implementar flujo completo de autenticación JWT y módulo de valoraciones físicas)


@dataclass
class Assessment:
<<<<<<< HEAD
    user_id: int
    answers: List[AssessmentAnswer]
    fitness_score: float
=======
    id: str
    user_id: str
    goal: FitnessGoal
    activity_level: ActivityLevel
    experience_level: ExperienceLevel
    height_cm: float
    weight_kg: float
    age: int
    fitness_score: Optional[float] = None
    created_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
>>>>>>> a8a4ebf (feat(auth,assessment): implementar flujo completo de autenticación JWT y módulo de valoraciones físicas)
