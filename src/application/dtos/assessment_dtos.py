from dataclasses import dataclass
from typing import List


@dataclass
class AnswerDTO:
    question_id: int
    answer: int


@dataclass
class SubmitAssessmentDTO:
    user_id: int
    answers: List[AnswerDTO]
