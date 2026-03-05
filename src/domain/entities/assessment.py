from dataclasses import dataclass
from typing import List


@dataclass
class AssessmentAnswer:
    question_id: int
    answer: int


@dataclass
class Assessment:
    user_id: int
    answers: List[AssessmentAnswer]
    fitness_score: float
